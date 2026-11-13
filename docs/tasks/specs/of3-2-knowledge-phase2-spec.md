# OF3-2 (phase 2 of the project-knowledge plan): the registry's answer life, the seam's bookkeeping, the conductor's door, project kinds, TR3-10 on the seam — SPEC (designer draft, round 2)

Designer (Opus), 13.11.2026, fix round t-464 after the critic-on-plan review `docs/tasks/specs/reviews/of3-2-knowledge-phase2-plan-review.md`
(t-463, verdict fit_with_fixes, 19 fixes). Round 1 was drafted on 1dfe10a; every `path:line` below was READ in this round on the worktree
`C:\QAFactory\forge-repo\.claude\worktrees\read-main` (origin/main, at or after fb36ae5), unless marked UNVERIFIED. P = that worktree's
`ai-packages/qa-factory`; owns lines name the live repo path `C:\QAFactory\forge-repo\ai-packages\qa-factory\...`.
Sources: node OF3-2 `plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:28` (status «ожидает»; OF3-1 :27 «ожидает»);
`plans/project-knowledge-plan.md` §2.1 (:50-69), §4 «Фаза 2» (:218-229), §7 (:319-366, the later word); the review; `docs/TESTING.md`.

## Review fixes -> where folded

| fix | where folded in this file (section, line) |
|---|---|
| F-A1 stand lessons share the registry | §0 F-5/F-6b L94-L96; §3 record L317, revoke L328; §4 L444, L448; §5 K1 L512, L537 |
| F-A2 `asked` is a marker; element rule for one-value keys; conflict at the seam | §3 states L264, element L286, `fact` L334-L365; §4 L452, L457, L478; §5 K3 L612; §6 F12a/F12b L879-L880 |
| F-A3 TR3-10: builders keep their road; two facts; walk_account; legacy DD row; stories in flight | §4 L481-L484; §5 K5 L703-L733; §7 Q-1 L908 |
| F-A4 in-story guard independent of the registry write | §4 L454; §5 K5 L713, L731 |
| F-A5 layer order (`need_fact` home) and the `offered` invariant | §5 K3 L616-L617 |
| F-A6 B-294 (a) through `human_word_check` | §0 F-21 L155; §5 K6 L751 |
| F-A7 honest scope of the no-silent-later-wins invariant; head-changed test | §3 heads L295; §4 L447; §5 K1 tests L512 (heads table) |
| F-A8 `remember` and kinds edges | §3 kinds L383, keys L284, `remember` L395-L418; §4 L465-L468; §5 K2 L567-L571 |
| F-A9 `remember` refuses keys that have a dedicated door | §3 `remember` L405; §4 L470; §5 K2 L567 |
| F-A10 only what has a phase-2 consumer; conductor.md cap | Digest L61; §2 L238; §5 K3 L612, K4 L683; §6 L865 |
| F-A11 K1 owns and names the pinned test edits | §5 K1 L523, L543 |
| F-B1 `_heads` replaces the loops of `roster`/`subjects`, serves `lessons` | §3 heads L295 |
| F-B2 legacy row after a phase-2 row; `supersedes` cycle | §3 heads L295; §4 L440-L441 |
| F-B3 fast test rows that drive `need_fact`; new texts through `human_text.problems` | §5 K3 tests L646; §5 K5 tests L729 |
| F-B4 `live-runs` rows | §5 K1 L563, K4 L699, K5 L747, K6 L787 (K3 and K2: none, nothing visible) |
| F-B5 `safe_direction` reader | §2 L238 (the "Not in phase 2" paragraph) |
| F-B6 driver-layers rows owned | §5 K3 L641 |
| F-B7 K1 before PK2-12 | §6 F14 L884; §7 L910 |
| F-B8 `remember`/`kind` reuse `_context`/`_write_prologue` | §5 K2 L572 |

## Digest

Phase 0 built the registry (§7 C1): `records/project-knowledge.json`, one writer `record` under a lock, `revoke`, provenance with the
person's words. Since round 1, SS1-11 added a sixth registry key (`environments.stand_lessons`) with its own idempotence. Phase 1 put the
catalogue into `config-keys.json` section `knowledge` (§7 C5). Phase 2 is therefore NOT a new store. After the review it is smaller:

1. **The registry learns an answer's life** (K1; plan 2.1, PK2-1, PK2-2). A row may carry a `condition` (the person's words, never parsed)
   and `supersedes` (the answers it replaces). The answer in force for a subject is its set of HEADS. Two heads are a CONFLICT that every
   reader hands over, never "the later one wins". A revoked head brings no older answer back, for every key, lessons and sides included
   (Lead F2 (a); owner question Q3). `asked` is a MARKER row, outside the answer graph. The new pure reader `fact()` gives the seam's
   step (C9).
2. **The seam's bookkeeping in the driver** (K3; plan 2.1/2.3, C7, C8). `Driver.need_fact` reads `fact()` for the facts a question is
   about, says whether to ask, and supplies the line "I asked this in <story> on <date> and got no answer then." `Driver.knowledge_asked`
   writes the `asked` markers. A question that holds no case waits by a catalogue field (`holds: none`), not by a list of kind names.
   The existing question builders keep their kinds, texts, price keys and executors (review F-A3).
3. **TR3-10 is the seam's first consumer** (K5). The way question and the data-change question read the registry before asking. An
   unanswered ask comes back in the next story with the earlier line. The kind tuple leaves `deferrable`. Their config writes stay the
   recorded writer they use today (`project_decisions` add/resolve — C2).
4. **The conductor's door** (K2, K4; plan 2.5). `project_knowledge.py remember` writes a config-stored fact only through
   `project_decisions` upsert + resolve, merging object values in code. Keys that already have a door (role, account, side, lesson) are
   refused with that door's name. The scope rule and the aloud line live in the conductor-actions row, because conductor.md has 3
   bytes of room.
5. **Project kinds** (K2; plan 2.6): `qa-factory/knowledge.json`, elements as registry rows, `show --contents`, carried by a reinstall.
6. **B-294 (a)** (K6): roles are refused `config_contract.py --record-approval|--apply`, `onboard_apply.py --apply`,
   `project_knowledge.py remember|kind`, in `human_word_check`.
7. **The missing map axis 37** "memory of a person's answer" (K7; §7 C3).

Moved to phase 3, because nothing in phase 2 consumes them (review F-A10, AR-22): the generic `knowledge` Person kind and its
`take_answer` branch; the price key `knowledge.first_need`; the F4 tokens (Lead decision on Q1 = (a)); the catalogue fields `question`,
`answer`, `person_class`, `while_unknown`, `safe_direction`; the "acting on your answer" line; the stand-scoped `not_needed` (FK-4 lift);
`needed_by` of a project kind and the role filter of `contents()`.

What a person sees change (everything else stays byte-for-byte as it is today):
- (K5) the S6 way question or data-change question, asked again in a later story after it got no answer, starts with one line: "I asked
  this in <story> on <date> and got no answer then." (Q2). A project that answered is not asked, as today (the config holds the
  answer).
- (K5) if the person's recorded answers about such a fact disagree, the question starts with one line naming both (Q2).
- (K1, K4) taking back an answer about a side or a lesson no longer brings the older one back; the conductor's line says the factory asks
  again (Q3).
- (K4) after the conductor records a free answer through `remember`, it says one line: "recorded as a rule of <the project | stand X>:
  <their words>; to undo, say so" (Q2).

---

## §0 Facts (read on read-main this round)

**Registry** (`P/scripts/project_knowledge.py`)
- F-1 `RECORD_REL` :45, `LOCK_REL` :46. `_derive_keys` :101-114 keeps only rows whose `store` is `registry` / `config+registry` (:107)
  and that carry `scope` and `compare` (:110). `KEYS, CATALOGUE_PROBLEM = _derive_keys()` :117.
- F-2 `STATES = (KNOWN, NOT_NEEDED, NOTICED)` :120; comment :119 "`asked` is RESERVED for phase 2 (no producer here)". `SOURCES` :121,
  `BY` :122.
- F-3 `_usable` :193-203 skips a row in a state outside STATES (:199) and a row with an empty element (:201). `_latest` :206-220 is
  later-wins (`(at, index)`); it returns None for an empty element form (:210-211).
- F-3b Four precedence loops: `_latest` (used by `_account_state` :282, `state` :298, `lessons` :476, `record` :694); `subjects` has its
  own loop (:413-419); `roster` has its own loop (:515-518).
- F-4 `record_problems` :619-676. The STATES refusal is at :632-633. Stand and side keys take `known` only (:634-635, the phase-0 FK-4
  deferral). The scope refusal is at :636-638. The side rules are at :642-651, the lesson branch at :652-653. A key that is neither a side
  nor a lesson goes through the ROLE rules (:654-664): an empty element is refused, the role form is checked, reserved names are refused.
  The empty-words door is at :669-673.
- F-5 `record` :679-709. Idempotence: the same state AND value returns the held row (:695); for `environments.stand_lessons` it must
  also be the same words (:696-700). The row shape is at :703-707.
- F-6 `revoke` :712-717 through `ER.revoke_row`.
- F-6b Lesson revive today: the docstring says revoking the newest row of a subject shows the previous live row again (:27-31).
  `cmd_revoke` :921-935 prints, for every key that is not a role or an account (sides AND lessons), "an older live row of the same
  subject, if any, is read again" (:933-934). The test is E44 at `test_project_knowledge.py:876-884`. Roles revive by the same `_latest`
  today, though their sentence (:930-931) says "it is asked again".
- F-7 `value()` :344-401. A config value that is present and not None reads `known` (:397-398). The template placeholder
  `manual.accounts_way.words: "not known"` and `data_way.may: "not known"` are at `P/references/templates/config.json:63-64`.
- F-8 `notice_from_handoff` :753-785 reads `roster()` (:769) outside the lock, then calls `record` (:775) — PK2-18.
- F-9 Catalogue `P/references/config-keys.json` section `knowledge` from :705. Six scoped registry rows (:706-711, `environments.stand_lessons`
  :711). The top-level `manual` row is at :729. No `manual.accounts_way` / `manual.data_way` / `manual.data_way.may` row exists.
  Count 79 rows (review run (1); not re-counted by me). The `about` text at :2 says "`ask_when` (null until the phase that asks)" and
  "for a registry row `scope` and `compare`".
- F-9b `report_facts.py` reads `PK.KEYS`: `_key_of_mark` :1986-1994 and `_registry_entries` :2175-2204 (`for key in sorted(PK.KEYS)`,
  `subjects` then `state`, only `known` subjects become entries). `test_gate_role_accounts.py:82` reads `PK.KEYS[key]["scope"]`.
- F-10 `_context` :817-837 (story -> project through `runtime_paths.project_for_task` :829); `_write_prologue` :844-856 (words, place,
  no_trace refusal).

**Asking today**
- F-11 `Person.__init__` (`P/scripts/driver_core.py:202-233`). It has no fact key. `offered` is "Set by `Driver.no_move` ALONE" (:210-212).
  `holds` is at :233. `no_hold` is an ad-hoc attribute: `driver-layers.json:1118` lists writers `walk_supply_person` /
  `data_change_person` and reader `deferrable`.
- F-12 `deferrable` (`P/scripts/driver_dialog.py:446-461`). Its first line (:456) is
  `if getattr(person, "no_hold", False) and person.kind in ("walk_supply", "data_change"): return True` (closed variety in code, AR-1).
  The D.1 docstring is at :453-455.
- F-13 Layers (`P/scripts/tests/fixtures/driver-layers.json:9`): driver_dialog < driver_conductor < driver_dispatch < the stage modules
  (driver_stage_s6 among them) < driver_gates < driver_machine. `Driver.say_once` lives in driver_dispatch (:974; def
  `driver_dispatch.py:2695`). State-key rows: `walk_supply_asked` :1197, `data_change_asked` :1199. Method rows: `walk_asked` :1023,
  `walk_ask_once` :1025, `walk_account_raise` :1033. `test_driver_layers.py:899-901` reports an ad-hoc row "used nowhere: delete it".
- F-14 TR3-10 (`P/scripts/driver_stage_s6.py`):
  - `walk_asked` :1439-1443 = a deferred item of the kind, or the `<kind>_asked` state key. It is one story's guard, and it does not
    depend on any registry write.
  - `walk_supply_raise` :1445-1464 asks `walk_supply` when `(short and not accounts.known) or (kinds and not data.known)` (:1453),
    over refs `["/manual/accounts_way", "/manual/data_way"]` (:1455). It asks `data_change` when `kinds and not data.may_known` (:1458)
    over `["/manual/data_way/may"]` (:1461).
  - `walk_ask_once` :1466-1487: `project_decisions.py add`; an open row of the same refs is reused; the row id goes to `build`.
  - The third caller is `walk_account_raise` :89-142 (call at :123, refs `/environments/<i>/credentials_by_role/<role>`).
  - Builders and executors are in `P/scripts/driver_dispatch.py`: `walk_supply_text` :3243, `walk_supply_person` :3270 (sets
    `state["walk_supply_asked"]`, `holds=()`, `no_hold=True` :3280), `_resolve_decision_row` :3283, `_answer_walk_supply` :3296 (merge on
    write :3320-3345), `data_change_text` :3370, `data_change_person` :3386, `_answer_data_change` :3397. Price keys `s6.walk_supply`
    :231, `s6.walk_account` :236, `s6.data_change` :241 of `P/references/question-prices.json`. Key names come from
    `config_contract.walk_supply_keys()` (`P/scripts/config_contract.py:825-827`).
  - `design/state-exits.md:204-205` hold the two questions' rows. :204 already says "a story that ends before gate B leaves the row
    open, and the next story's first need asks it again on the same row".
- F-15 Stand-gap `accept always` -> `environment_record`: not re-read (it is a non-goal reference only).
- F-16 `P/references/conductor-actions.json` `actions`. The phase-0/SS1-11 doors are :26-30 (account, role, side, lesson, revoke; no
  `id`). The TR3-10 rows `walk_supply_way` / `walk_account_words` / `data_change_words` are at :37-39; :37 carries the "MERGE ON WRITE"
  discipline.
- F-17 conductor.md is 11897 bytes; the cap is 12000 with a mandatory 100-byte margin (`test_conductor_doors.py:31`, :161; review run
  (3)). `AWAITING_ITS_SITE` is at :634, `census_problems` at :668.

**Writing the config (§7 C2)**
- F-19 `project_decisions.upsert` (`P/scripts/project_decisions.py:400-432`) refuses an empty `asked` (:403). It reuses an open row only
  when the stored refs SET-EQUALS the new refs (:421-423). `resolve` (:450-523) needs a value for EVERY pointer (:464-466) and assigns
  each value WHOLE (`_set_pointer` :471-472). It writes the receipt with `recorded_at`/`before` (:495-506) and the config only on a
  change (:509-510). It does not read `no_trace` (a case-sensitive grep for `closed_by_run|no_trace` gave no hit; positive control: the
  same call shape found `closed_by_run` in project_knowledge.py:558).
- F-20 `config_contract.recorded_writes` keeps receipted writes across `restore_config` (config_contract.py:2350-2414, review-verified;
  not re-read by me).

**Guard** (`P/scripts/guard_pre_tool.py`)
- F-21 `HUMAN_WORD_MSG` :1726-1755 (the project_knowledge sentences :1740-1747). `human_word_check` :1758-1803; the project_knowledge
  regex is :1789 and already holds `account|role|revoke|side|lesson`; a role is refused at :1800-1803. The sanction table only exempts
  scripts from the `config.json`-target detector (review F-21); it is not touched here. Two argparse parsers accept abbreviations:
  - `config_contract.py main` :2975-2997 has options `--root --migration-plan --apply --record-approval --approval-ref --evidence-ref
    --fold --validate --price-table-answer --answers --model-id --check-environment`;
  - `onboard_apply.py` :1913-1928 has `--apply` beside `--approval-ref`, `--also-retire`, `--answers`.
- F-22 The main session is never refused by the config guard (comment :1894-1899, review-verified).
- F-22b `judgment-census.json`: `human_word_check` is `safety`, owner intent (:423); `project_knowledge.py:_refuse_no_trace` is `safety`
  (:783); `record_problems` is `shape`, owner data (:784). Ceilinged classes are only `word-list, meaning-proxy, meaning, safety`
  (`test_judgment_census.py:93`); `shape` and `xref` carry no ceiling. `deferrable` is not a census unit (grep; control: :783 found).

**Records, install, map, tests**
- F-23 `P/references/install-paths.json`: `qa-factory/config.json` carried (:32), registry carried (:56); no `knowledge.json` row.
  `P/references/artifact-writers.json` lists neither records nor config.json (case-insensitive grep; control: its `"artifacts"` keys
  found).
- F-24 `docs/SIBLING_MAP.md`: the last axis is 36 (:606); no axis 37 (grep `^## Axis 3[3-9]` found 33-36 only).
- F-25 `P/scripts/tests/test-layers.json` keep rows: `test_conductor_doors.py` :670, `test_config_migration.py` :739,
  `test_driver_layers.py` :1385, `test_guard_project_knowledge.py` :2170, `test_guard_write_owners.py` :2198,
  `test_human_questions.py` :2457, `test_install_paths.py` :2645, `test_project_knowledge.py` :3976, `test_state_exits.py` :5370,
  `test_walk_supply.py` :6579 (gate_named; covers the driver set). Red at quarantine entry (`keep_fail_at_entry` :7014-7025):
  `test_conductor_doors.py`, `test_driver_layers.py`. Slow (`P/scripts/slow_tests.json`): `test_config_migration.py` 17.7,
  `test_guard_write_owners.py` 10.8, `test_install_paths.py` 14.2, `test_judgment_census.py` 33.3 — judged by CI. `test_walk_supply.py`
  and `test_project_knowledge.py` are not in it.
- F-25b Pinned expectations K1 turns red: `test_keys_are_derived_from_the_catalogue_in_todays_order`
  (`test_project_knowledge.py:995-1004`); `test_config_only_key_refused_with_todays_text` (:1007-1012, the key list inside the text);
  E44 (:876-884); `test_config_migration.py:405-407` (R1 "every row carries ... a null ask_when (phase 1 fields only)").
  `test_asked_row_is_skipped` (:267-275) STAYS green under K1's design (asked stays refused for `product.roles`, and an asked row never
  lifts or suppresses). R1's top-level rule (`knowledge_gaps` :370-386) ignores dotted rows, so `manual.accounts_way` needs no
  `in_template`.
- F-26 Phase 1 node f is not on main (`knowledge-read-baseline.json` absent; review run).
- `test_walk_supply.py` builds a bare driver (`Rig` :29-74); D.1 rows :86-120 use `walk_supply_person` and `del plain.no_hold`.
- `test_words_doors.py` is a SCAN of inline `--decision|--words|--text|--note` doors (:61-62, :114-115), not per-command rows; the new
  commands take `--words-file` only, so it needs no row.

**Premises measured**
- M-1 (measured by the review, run (2)): the one real-run question log (`fixtures/stories/local-1-arm-b/state/driver-questions.jsonl`) has
  37 lines and no S6 supply question. The fixtures cannot measure what the seam saves; the measurer is phase 6.2.
- M-2 UNMEASURED (the stand copy is outside the repo): subjects with two or more live rows in a real registry. Under F1 (a) the answer
  does not change behaviour (legacy rows stay later-wins); it only sizes how many legacy subjects exist.

---

## §1 AR-n touched, owners and census classes, FR sections

| AR | How OF3-2 keeps it | Change check in the DoD |
|---|---|---|
| AR-1 | the TR3-10 kind tuple in `deferrable` (driver_dialog.py:456) becomes the catalogue field `holds: "none"`, read by key through `PK.holds_none` | K3 rows: a Person with `no_hold` and `fact_keys` whose rows say `holds: none` is deferrable, and the same flag on a gate Person is asked at once. K5 deletes the tuple; K5's report greps `"walk_supply", "data_change"` over P/scripts (positive control: the same grep run before the edit finds driver_dialog.py:456) |
| AR-3 | a config-stored fact keeps the config as its carrier; the seam and `remember` write it only through the recorded writer | K2 red-first row "a fact remembered in a story is alive after `restore_config`" (C2) |
| AR-13 | the registry is read only through `state`/`value`/`fact`/`subjects`/`roster`/`lessons`/`kinds`/`contents`, all over ONE precedence helper `_heads`; a fact whose known-ness has its own reader (`config_contract.walk_supply`) is judged by it (F9) | K1 row set; the report greps `project-knowledge.json` and `knowledge.json` reads outside project_knowledge.py (positive control: `install-paths.json:56` found by the same grep) |
| AR-14 | one writer of the registry (`record`), one of `knowledge.json` (`record_kind`); `remember` calls `project_decisions` for the config and never writes `config.json` itself; keys with a dedicated door are refused by `remember`; the guard closes the new write commands to roles | K2 rows; K6 rows |
| AR-15 | one road for "a person's answer kept across stories": registry + `fact()`; TR3-10's config write stays the `project_decisions` road (the recorded writer, shared with `remember`) | K5 rows; axis 37 (K7) lists every carrier |
| AR-16 | the TR3-10 questions keep their `closed_question` builders; the earlier line is part of the same text | K5 row: the text with the line passes `human_text.problems` and its body hash differs (FR-7) |
| AR-20 | `driver-layers.json` gains method rows; `need_fact` lives in driver_dispatch (no upward edge); the ad-hoc `no_hold` row goes because the attribute becomes formal; no ratchet raise | builder STOPs on any upward-edge or ratchet raise and lists added rows |
| AR-22 | every new catalogue field has a phase-2 reader (§2); fields without one wait for phase 3 | K1 data-join row over the `first_need` rows |
| AR-23 | empty outcomes: no registry rows = `fact` step `unknown`, problem ""; a list key asked without an element = `unknown` with a problem; `contents()` with no kinds = factory lists plus the line "the project has defined no kinds of its own" | K1/K2 rows |
| AR-24 | the person's words reach the registry whole (`--words-file`); a `condition` is their words, whole, never parsed | K1/K2 rows |
| AR-25 | `asked` gets a `state-exits.md` row; a conflict (computed) exits by a superseding answer or `revoke` | K1 row in `state-exits.md`; `test_state_exits.py` green |
| AR-28 | `fact()` errs toward asking (§3 adversarial inputs) | K1 parameterised row set |
| AR-29 | code checks data only; the scope of a free answer and whether a condition applies are the conductor's / role's judgment | census table below |

Owners and census classes of every check this spec adds or alters (CLAUDE.md rule 10, P27, AR-29):

| check | where | owner | census class (row) | ceiling |
|---|---|---|---|---|
| `record_problems` (altered: `asked` marker rules, one-value element rule, role rules only for `role_form` keys, `supersedes` ids of the same subject, `condition` is text, dynamic `project:<kind>` keys) | project_knowledge.py | data | `shape`, existing row judgment-census.json:784, class unchanged | `shape` has none — met |
| `kind_problems` (new: name form, `says` one line, `scope` in {project, stand}, scope change refused while elements live) | project_knowledge.py | data | new row `shape`, roles `["conductor"]` | none — met |
| `remember` refusals (new unit: catalogue key join, dedicated-door keys, stand name join, kind join, values file form) | project_knowledge.py | data | new row `xref`, roles `["conductor"]` | `xref` has none — met |
| `fact()`, `holds_none()`, `Driver.need_fact`, `Driver.knowledge_asked` | project_knowledge.py, driver_dispatch.py | data | not units (they refuse nothing and raise no Person) | — |
| `deferrable` first line (altered) | driver_dialog.py | data | not a census unit (F-22b) | — |
| `human_word_check` (extended: four more command shapes) | guard_pre_tool.py | intent (only the person's onboarding approves; only the conductor records a person's word) | existing unit, `safety`, row :423; NO new unit | `safety` count unchanged — met; a new unit would be a raise R-1 that needs approval BEFORE dispatch |
| the scope of a free answer (В3) | conductor-actions row (role text) | judgment (conductor), accepted by the person (aloud line, revoke) | none | — |
| whether a `condition` applies to a story | the reading role / conductor | judgment | none | — |

No raise of `judgment-census.json` ceilings, `NO_MOVE_BASELINE` or `role-load.json` is expected or approved, except R-1 if it arises.

FR sections walked: A (FR-1/FR-2: every new refusal names what it expected and a door its receiver can use; FR-57), B (FR-6/FR-7: a
question asked again in a later story changes its text; FR-8: words whole), C (FR-13: kinds and fields are data; FR-38: the conductor's
requirements are in its row; FR-39: the main session is never refused), D (FR-59: unknown -> ask or the declared default), E (FR-41: an
unreadable registry is named, never empty), F (FR-53: a `no_trace` story writes no registry row — `_refuse_no_trace`), G (FR-30
English, FR-32, FR-54 siblings by the map).

---

## §2 Catalogue fields in phase 2 (`config-keys.json` section `knowledge`) [F-A10] [F-B5]

Only fields with a phase-2 reader (AR-22). Values go ONLY on the three new rows. Every other row keeps its exact bytes, which leaves
nothing to conflict with phase-1 node f.

| field | values | phase-2 reader | rows |
|---|---|---|---|
| `scope` (exists; the plan's `about`) | `project` · `stand` | `_derive_keys` (a row with `scope` and `compare` is a registry key), `record_problems`, `fact` | + the three new rows: `project` |
| `compare` (exists) | `role_form` · `exact` | `_form` | + the three new rows: `exact` |
| `value` | `one` · `list`; ABSENT = `list` (today's element-per-row rule) | `_usable` / `record_problems` element rule; `contents()` (lists only) | the three new rows: `one` |
| `ask_when` (exists, null) | `first_need` on the three new rows; `null` elsewhere | `Driver.need_fact` (a key without it is not a seam fact: the caller keeps its own road) | the three new rows |
| `holds` | `none` | `PK.holds_none` -> `deferrable` | the three new rows |

The three new rows go right after `environments.stand_lessons` (:711), in this order. All three carry `"store": "config:<path>"`,
`"scope": "project"`, `"compare": "exact"`, `"value": "one"`, `"ask_when": "first_need"` and `"holds": "none"`:
- `manual.accounts_way` (store `config:manual.accounts_way`), `needed_by` `["config_contract.py:walk_supply",
  "driver_stage_s6.py:walk_supply_raise"]`;
- `manual.data_way`, the same `needed_by`;
- `manual.data_way.may`, the same `needed_by`.

Not in phase 2, each with its first consumer: `question`, `answer`, `person_class` (the generic knowledge Person, phase 3 — queue Q-2);
`while_unknown` and `safe_direction` (F-B5: no phase-2 runtime reader exists — the TR3-10 callers act their default as today, so C10 lands
with the first gate-A key in phase 3); `derive` (F8, phase 4.2). `about` stays `scope`.

## §3 The registry (K1, K2) — `scripts/project_knowledge.py`

**States and the marker [F-A2].** Answer states stay `STATES = (KNOWN, NOT_NEEDED, NOTICED)`. A new MARKER state `ASKED = "asked"` is NOT
added to `STATES`: `_usable` (answers) keeps rejecting it, so `roster`, `subjects`, `lessons` and `_account_state` never see a marker.
A marker is read only by `_asked_rows` and `fact()`.

Marker row shape: `{id, key, environment, element, state: "asked", scope, value: null, provenance{source: "factory", words: "", story,
by: "driver", where}, at}`. It has NO `supersedes` and NO `condition` key (fork F12c covers the source word).

A marker is legal only for a key whose catalogue row says `ask_when: "first_need"`. Any other key is refused with a text that contains
`asked`: "the state 'asked' is written only by the driver, for a fact the catalogue asks at first need; <key> is not one; nothing was
recorded". That keeps `test_asked_row_is_skipped` green. Idempotence: a marker of the same subject and the same story returns the held
row (`created` False).

**Keys (K1).** `_derive_keys` takes EVERY catalogue row with a non-empty string `scope` and `compare`, not only registry stores. Each
KEYS entry keeps the shape `{"scope", "compare"}`. The other fields are read through a new `_row(key)` (the catalogue row through
`rows(key)`).
- POSITIONAL invariant: the six registry rows come first in file order, so `list(KEYS)` begins with today's six and the three new keys
  follow.
- A row without `scope` is not a registry key; `record_problems` refuses it with today's text shape (the key list now names nine keys).
- A damaged catalogue follows today's `CATALOGUE_PROBLEM` road.
- K2 adds the dynamic keys `project:<name>` from `knowledge.json` through `_keys_for(root)` (KEYS plus one `{scope: <kind's>, compare:
  "exact"}` per kind). Every reader that takes `root` passes it to `_usable`, `_form`, `record_problems`, `subjects` (F-A8 f).

**Element rule [F-A2 iii].** A key whose row says `value: "one"` takes the element `""` exactly (fork F12b), and `_heads` accepts the
empty form for it. A list key (no `value`, or `list`) needs a non-empty element, as today. The ROLE rules (:654-664) apply only to keys
whose `compare` is `role_form`. A `project:<kind>` element follows the side-name form rules (non-blank; no space at an end; no control
character; at most 80 characters) — small choice.

**Row fields (K1).** Every answer row written by phase-2 `record` carries `condition` (a string, `""` = none) and `supersedes` (a list
of row ids, fork F12a; `[]` = "I read no answer"). Neither field is ever parsed. A `condition` is stripped of blank space at its ends and
otherwise stored whole. It is returned by `state()`, `value()`, `fact()` and by roster entries.

**Heads [F-A7] [F-B1] [F-B2].** A new `_heads(rows, key, environment, element, keys) -> (heads: list, cycle: bool)` is the ONE precedence
of this module. `_latest` is deleted. Every caller moves to `_head()`, which returns one head, or None plus the conflicting ids:
`state`, `_account_state`, `record`, `lessons`. The own loops of `subjects` (:413-419) and `roster` (:515-518) are replaced by it.
- Live answer rows of the subject: `_usable` and the same subject (environment exact, element by the key's comparator).
- SUPERSEDED = (a) every id in the `supersedes` list of ANY answer row of the subject, revoked or not. A revoked row keeps superseding
  what it superseded: this is Lead F2 (a), nothing comes back by itself. Plus (b) for every LEGACY answer row (one with no `supersedes`
  key, revoked or not), every answer row of the subject that is older by `(at, index)` (Lead F1 (a): later-wins as today). A legacy row
  written AFTER a phase-2 row (an older plugin on a teammate's machine) follows the same rule, so it becomes the head.
- HEADS = live rows minus superseded. One head: it decides. Two or more: a CONFLICT. Zero heads while live rows exist (a cycle or a
  self-link written by hand): `cycle` True, the subject reads `unknown` with the problem "the answers about <key> <element> point at each
  other (<ids>); `project_knowledge.py show` lists them".
- In conflict: `state()` / `value()` return `unknown` with `conflicts: [ids]`. `subjects`, `roster` and `lessons` leave the subject out of
  their answer lists and add it to a new `conflicts` output list (toward asking; nothing picks one).
- `record(..., supersedes=MISSING)`. MISSING means the writer named nothing (every phase-0 door, `remember` without `--supersedes`). The
  row then supersedes EVERY head found under the lock: it is the person's newest word on the subject. An explicit list is stored as
  given.
- INVARIANT (honest scope, F-A7): between rows whose writers NAMED what they read, the later never wins silently. A writer that names a
  head which is no longer the head creates a conflict, not an overwrite. A writer that names nothing settles the subject.

**`record(root, *, key, environment, element, state, scope, value, words, source, story, by, where="", task_root=None, condition="",
supersedes=MISSING)`** (K1). Under the lock, as today: `load` -> `record_problems(..., rows=rows, supersedes=..., condition=...,
keys=...)` -> `_refuse_no_trace`. Answer rows are idempotent when the single head has the same state, value and condition, and, for
`environments.stand_lessons`, the same words (F-5, kept [F-A1]), and `supersedes` is MISSING or equals `[head id]`. Then the held row is
returned with `created` False. Otherwise a new row is written.

`record_problems` additions (keyword-only, so today's positional callers are unchanged):
- a `supersedes` id that is not a row of the SAME subject, or the new row's own id -> refused: "PK-9 is not an answer about <key>
  <element><on stand>; nothing was recorded; `project_knowledge.py show` lists the ids";
- a `condition` that is not a string -> refused;
- the marker rules above.

The stand and side `known`-only rule (:634-635) is UNCHANGED: the FK-4 lift has no phase-2 consumer.

**Revoke [F-A1].** `revoke` is unchanged. Under the heads rule, revoking the only head makes the subject read `unknown`, for every key.
- The `cmd_revoke` sentence for non-role keys (:933-934) becomes: "<id> is taken back (<key> <element>): it is no longer read, and no
  older answer comes back; the factory asks again where it needs it (`project_knowledge.py show` lists the rows)."
- The docstring :27-31 becomes "A lesson leaves with `revoke`; no older lesson of the subject comes back".
- The role/account sentence (:930-931) stays as it is: it now matches the code.

**`fact(root, key, environment="", element="", story="", known=None, cfg=None) -> dict`** (K1). PURE: it never raises and writes nothing
(C9). It returns `{"step", "row", "conflicts", "condition", "asked", "problem"}`. `step` is one of `known` · `not_needed` · `asked_here` ·
`asked_before` · `unknown`.

ORDER (POSITIONAL invariant: the catalogue is read first, so a key with no row never reads `known`; the carrier is read before the
registry, so the registry never makes a config-stored fact `known`):
1. No catalogue row, or a damaged catalogue -> `unknown` with the problem.
2. A list key (`value` absent or `list`) with element `""` -> `unknown`, problem "<key> is a list; name the element (`show --contents`
   lists them)" [AR-23].
3. The carrier. For a config-stored key (`store` starts `config:`): the caller's `known` (bool) decides (Lead F9 (a)); without it,
   `value()` decides. `known` -> step `known`, and the single registry head's `condition`, if any, is returned beside it (data only).
   For a registry-stored key, nothing happens at this step.
4. The registry heads.
   - A conflict -> `unknown` with `conflicts`. A cycle -> `unknown` with the problem.
   - A single head `not_needed` with condition `""` -> step `not_needed`.
   - A single head `not_needed` WITH a condition -> not used to suppress; it is handed over as `row`.
   - A single head `known`: for a REGISTRY-stored key -> step `known`; for a CONFIG-stored key it NEVER yields `known` [F-A2 iv] (the
     carrier decided at step 3). It is handed over as `row`.
   - A single head `noticed_unconfirmed` -> handed over as `row`.
5. The marker. The newest marker of the subject that is newer (by `(at, index)`) than every head, or any marker when there is no head:
   with `provenance.story == story` (non-empty) -> `asked_here`; otherwise -> `asked_before`. The marker row is returned as `asked`.
6. Otherwise -> `unknown`.

ERROR DIRECTION. This reader now SUPPRESSES questions for a key (a more consequential role than phase 0's roles-only road), so it may
err only toward asking. These adversarial inputs must give `unknown` / `asked_before` and never `known` / `not_needed`. Each is a row of
ONE parameterised test, whose id is the input:
- an unreadable registry; a registry of another `schema_version`; a damaged catalogue; a key with no row;
- a revoked head; a head of another scope; a head on another stand (the exact name, with the case differing);
- a `not_needed` head WITH a condition; two heads (conflict); a cycle or a self-link; a `noticed_unconfirmed` head;
- an `asked` marker of another story; an `asked` marker with an empty story;
- a placeholder config value with `known=False` from the caller; `value()` known while the caller says `known=False`;
- a config-stored key with a registry `known` head while the caller says `known=False` [F-A2 iv];
- an `asked` marker newer than a conditional `not_needed` head: the head is still handed over, and the marker never hides it
  [F-A2 i, F7].

**`holds_none(keys) -> bool`** (K1). PURE. It is True only when `keys` is non-empty and EVERY key has a catalogue row with
`holds: "none"`. A damaged catalogue or a missing row gives False. Error direction: False = the question is asked at once, never
withheld.

**Project kinds (K2).** The file is `qa-factory/knowledge.json` (Lead F11 (a)). It is absent until the first `kind` command. Shape:
`{"schema_version": 1, "kinds": {"<name>": {"says": "<one line>", "scope": "project"|"stand", "by": "conductor", "words": "<the person's
words>", "story": "<id>", "at": "<iso>", "history": [<earlier whole kind objects>]}}}` (`history`: fork F12e).
- `kinds(root) -> {"kinds", "problem"}` is the ONE reader, and pure. An absent file gives `{}` and `""`. An unreadable file, one that is
  not an object, or one of another schema gives `{}` and the problem.
- `record_kind(root, *, name, says, scope, words, story, by="conductor", task_root=None)` writes under the SAME lock as `record`. It
  refuses through `kind_problems`:
  - the name: 1-60 characters of letters, digits, space, `-` and `_`, not starting with a digit, unique among kinds after case-folding;
  - `says`: one line of 1-200 characters;
  - `scope`;
  - a scope change while the kind has live elements -> refused, door "take its elements back with `revoke` first" [F-A8 e];
  - empty words -> the `person_words.door` text;
  - `_refuse_no_trace`;
  - an unreadable file is never written over (door `show`).
  The same fields again -> the existing kind, `created` False. A changed `says` -> the previous whole object is appended to `history`
  and the new fields replace it (F12e (a)).
- Elements are registry rows of key `project:<name>` (fork F12d), written by `remember`. `record_problems` accepts the key only when
  `kinds()` holds the name; the scope comes from the kind.
- `contents(root) -> list[{"name", "says", "path", "elements"}]`: one entry per catalogue LIST key with live elements and one per project
  kind. `path` is the file. `elements` is a COUNT, never the values (FR-15). No kinds -> the factory entries plus the line "the project
  has defined no kinds of its own". There is no role filter (phase 5).

**The conductor's door (K2) — `remember` [F-A8] [F-A9].**

CLI: `project_knowledge.py remember --task T (--values-file F | --not-needed --key K | --key project:<kind> --element E) [--stand N]
--scope project|stand|story [--condition-file C] [--supersedes PK-n[,PK-m] | --supersedes none] --words-file W`. Its prologue is
`_write_prologue` (F-B8): words, then place through `_context` / `runtime_paths.project_for_task`, then the `no_trace` refusal.

The steps, in order:
1. `--scope story` -> refused, door `waiver.py --task <T> --stage <S> --block "<block>" --words-file <file>` (a story-only answer is a
   waiver).
2. Keys that have a dedicated door are refused, naming the door: `product.roles` -> `role`; `environments.credentials_by_role` ->
   `account`; the three side keys -> `side`; `environments.stand_lessons` -> `lesson` [F-A9].
3. `--values-file` holds a JSON OBJECT `{<catalogue key>: <value>, ...}`. Every key must be a config-stored catalogue row
   (`store: config:<path>`). The file is refused with exit 2 and the door "write the file as a JSON object of catalogue keys and values
   (`project_knowledge.py show --contents` names the keys)", nothing written, when it is:
   - empty, not JSON, not an object, or an empty object;
   - holding a key that is not config-stored or not in the catalogue [F-A8 a].
4. Scope check: the scope of each key is its catalogue `scope`, else `stand` for a path under `environments[]` and `project` otherwise.
   A mismatch with `--scope` -> refused, naming the key's scope.
5. Pointers: `config:a.b` -> `/a/b`. `environments[].x` -> `/environments/<index>/x`, with the stand resolved by NAME through
   `environment(name)` at write time. A stand not found, twinned, or `environments` not a list -> refused, nothing written.
6. Merge [F-A8 c]: an OBJECT value is merged into the config's CURRENT object at that pointer (a deep copy; `{}` when the current value is
   not an object), with only the given keys replaced. Any other value is assigned whole.
7. `project_decisions.upsert(field_refs=<all pointers of the call>, essence="a lasting answer about <keys>", asked="recorded by the
   conductor in <story>: <first line of the words, 160 chars>", scope="project", owner="user")` [F-A8 d]. Because `upsert` compares the
   refs as a SET, a legacy open row with the same pointers is reused [F-A3 c]. Then `project_decisions.resolve(<id>, <words>,
   "<story> remember", {pointer: value})`, which writes the receipt (C2).
8. Registry, AFTER the config: a `known` row (value `null`) is written ONLY when `--condition-file` is non-empty, because the receipt
   cannot hold a condition. A key without a catalogue `scope` then refuses the condition BEFORE step 7: "the catalogue gives <key> no
   scope yet, so a condition cannot be kept beside it; record the value without it, and keep the condition in this story's waiver";
   nothing is written.
9. `--not-needed --key K` writes NO config value [F-A8 b] and one registry `not_needed` row. K must be in KEYS with project scope;
   otherwise it is refused, naming why.
10. `--key project:<kind> --element E` writes one registry `known` row (value `null`, scope from the kind, `--stand` for a stand kind).
11. Partial failure: resolve fails -> nothing written, exit 2 with the resolve message. Resolve succeeds and the registry write is
    refused (lock, no_trace) -> exit 2 with the line "the settings hold it; the record of earlier answers does not; run the same command
    again". This is config first, registry second, the order of today's `account` door.
12. `--supersedes` is passed to `record` as a list; `none` means `[]`; when absent, MISSING.

`project_knowledge.py kind --task T --name N --says-file F --scope project|stand --words-file W`; `project_knowledge.py show --contents`.

## §4 Edges (behaviour and the invariant each protects)

| edge | behaviour | invariant |
|---|---|---|
| a legacy row (no `supersedes`) | it supersedes every older row of its subject (F1 a) | no existing registry turns into conflicts on upgrade |
| a legacy row written after a phase-2 row [F-B2] | the same rule: it supersedes every older row, so it becomes the head | one deterministic precedence on every machine |
| a `supersedes` cycle or self-link (hand edit) [F-B2] | `unknown` + problem naming the ids | a broken link never reads as an answer |
| `supersedes` names a revoked row | allowed; a revoked row keeps its own links | a revoke never blocks a new answer, and never revives an older one |
| `supersedes` names a row of another subject, an unknown id or itself | refused, nothing written, door `show` | a link never ties two facts together |
| revoke of the only head (lessons, sides and roles included) [F-A1] | the subject reads `unknown` (F2 a, Q3 a) | an old answer never comes back by itself |
| revoke during a conflict | the remaining heads decide; when one is left, it decides | a conflict exits by revoke or by a superseding answer (AR-25) |
| a phase-0 door into a conflicted subject | supersedes every head (MISSING) | the person's newest word settles it |
| a writer names a head that changed after it read [F-A7] | a conflict; both heads listed | the later answer never wins silently over one its writer did not see |
| a lesson corrected with new words, same subject | a new row (words take part in idempotence) [F-A1] | a lesson's words are its payload |
| `condition` empty, blank or None | stored `""` | an unconditional answer is unchanged by the field |
| `condition` long, with line breaks, non-Latin | stored whole | the person's words are never cut in the store (FR-8) |
| a `not_needed` head with a condition | never suppresses (fact step 4); handed over as `row` | code never decides that a condition applies (P27) |
| an `asked` marker newer than an answer [F-A2 i] | it never supersedes, never hides the answer; `roster` / `subjects` / `lessons` never list it | a marker is not an answer |
| an `asked` marker for a key without `first_need` | refused (text names `asked`); a hand-written one is skipped by every reader | a marker exists only where the seam asks |
| the `asked` write refused (no_trace, lock) [F-A4] | one note (`say_once`); the question is still raised; in-story re-ask is still prevented by `walk_asked` (deferred item or `<kind>_asked` state key, F-14), which never depends on the registry | an experiment leaves no trace (P8), and FR-7 holds within the story |
| an `asked` marker, then the story ends unanswered | next story: `asked_before` -> the question is asked again with the earlier line | a question asked again changes its text (FR-7); the unanswered state has a way out (AR-25) |
| two stories mark the same fact | two markers; the newest decides `asked_before`'s date | — |
| a config-stored key with a registry `known` head, config value absent or a placeholder [F-A2 iv] | `unknown` | the value carrier decides known-ness |
| a placeholder value (`"not known"`) | the caller's `known=False` -> `unknown` (F9 a) | a placeholder never reads as an answer |
| a damaged catalogue | `fact()` `unknown`; `need_fact` returns `seam: False` and the caller keeps today's road; `holds_none` False (the question is asked at once); `record` refuses with the damage sentence | a damaged table never asks a wrong question or records a fact |
| a catalogue row with `ask_when: first_need` and no `holds` | `holds_none` False: asked at once, not deferred | a question is never withheld by a missing field |
| `no_hold` set on a Person with no `fact_keys`, or on a gate / exit-4 Person | falls through to the holds test: asked at once | a flag set by mistake never withholds a question (D.1) |
| knowledge.json absent (TEMPORAL: before the first `kind`) | `kinds()` `{}`; `project:<x>` refused "the project defines no kind named <x>; create it with `project_knowledge.py kind`"; `contents()` lists the factory lists only | absent is not unreadable |
| knowledge.json unreadable, not an object, or another schema | `kinds()` `{}` + problem; `record_kind` refuses to write over it (door `show`); `project:<x>` refused naming the problem | a damaged file is never overwritten (FR-41) |
| kind names that are twins by case, or blank | refused | one kind, one name |
| a kind's scope change while elements live [F-A8 e] | refused, door: revoke the elements first | no element is stranded by a scope mismatch |
| `remember` values file empty, not JSON, not an object, or with an unknown key [F-A8 a] | exit 2, nothing written, door | a malformed value is never written |
| `remember --not-needed` on a config key [F-A8 b] | registry `not_needed` row only; the config keeps its value or placeholder | the config holds values; the registry holds what a value cannot say |
| `remember` with an object value [F-A8 c] | merged into the current object | a key the answer does not name is never lost (today's MERGE ON WRITE, now in code) |
| `remember` on two config keys whose legacy open DD row has the same pointers [F-A3 c] | `upsert` reuses that row (set equality) | an old open row is reused, never duplicated |
| `remember` on a key with a dedicated door [F-A9] | refused, naming the door | one road per key (P31, AR-14) |
| `remember` `--condition-file` on a config key with no catalogue scope | refused before any write | a condition is never dropped silently |
| `remember` resolve OK, registry refused | exit 2, the line names the half written | config first, registry second; the person is told what holds |
| `remember --scope story` | refused, waiver door | a story-only answer is the story's |
| `remember` or `kind` run by a role | guard refusal (K6) | one writer of a person's words (AR-14, P15) |
| `remember` / `kind` in a `no_trace` story | refused by `_write_prologue` | P8 |
| the conductor edits `config.json` by hand | not refused (F-22); `restore_config` reverts an unrecorded write at story end; the conductor row says so (F5 a) | a fact meant to last goes through the door |
| phase-1 node f not merged (TEMPORAL) | K1 does not start (F10 a) | the plan's order 1 -> 2 |
| K1 merged alone (TEMPORAL) [F-A2] | nothing writes markers yet; a hand-written marker is skipped by every answer reader | K1 changes no visible behaviour except revoke (Q3) |
| K3 merged, K5 not (TEMPORAL) | the tuple stays in `deferrable` beside the catalogue road; the TR3-10 Persons carry no `fact_keys` and keep their road | no world where the two S6 questions lose their deferral |
| K5 merged | the tuple is gone; both builders set `fact_keys`; the catalogue rows say `holds: none` | one road (AR-1) |
| an open TR3-10 DD row from before K5 [F-A3 c] | K5 keeps `walk_ask_once`, so the raise reuses it as today (state-exits.md:204 "asks it again on the same row") | an old open row is reused, never duplicated |
| a story in flight across the K5 upgrade [F-A3 d] | `walk_supply_asked` / `data_change_asked` and deferred items of those kinds keep their meaning: K5 changes neither the state keys nor the executors | an answer to a question asked before the upgrade still has its executor |
| `walk_supply` with accounts known and data unknown [F-A3 a] | asked, as today; `need_fact` gets only the unknown facts | today's trigger (:1453) is kept |
| `walk_account` (third TR3-10 question) [F-A3 b] | unchanged: DD road, no marker, no earlier line; queued as node Q-1 (§7) | a residual is a node with owns and a test (P31) |
| report_facts reads `PK.KEYS` (F-9b) | the three new keys are listed; their markers and `not_needed` rows never become entries (only `known` subjects do); a conditional `known` row of a config key becomes an entry with use `unmeasured` | a marker is never counted as a known fact |

## §5 Nodes

Every test is a row in an EXISTING keep file (F-25). No new test file, no source pin, no in-test negative control, and no mutation list
(docs/TESTING.md: mutations are judged by the canon). Test lines stay within the node's code lines, or the report gives one line of reason.
Red-first: each node's first commit adds its behaviour rows red.

DoD for every node:
- its rows are green, and the verification run is attached verbatim:
  `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` and
  `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`;
- slow files (`slow_tests.json`: `test_config_migration.py`, `test_guard_write_owners.py`, `test_install_paths.py`,
  `test_judgment_census.py`) are judged by CI only;
- a keep file red at quarantine entry (`test_conductor_doors.py`, `test_driver_layers.py`) is reported by the row ids that name this
  node's code; the node is judged on its own rows;
- package commits carry `architecture: AR-n -- <how kept>` and `judgment:` lines.

STOP and return when:
- a ratchet raise is not listed;
- a test expectation must change that is not named in the node;
- a reader's error direction cannot be kept;
- a role text (`agents/`, `phases/`, skills) names a command this spec closes (K6).

Hot files are named per node with their functions. `story_run.py`, `hooklib.py`, `stage_guard.py`, `gate_preflight.py`, `controller.py`,
`brief_pack.py`, `config_contract.py`, `report_facts.py` and `driver_machine.py` are NOT written by any node.

### K1 — the registry's answer life (plan 2.1, PK2-1, PK2-2; C1, C9) [F-A1] [F-A2] [F-A7] [F-A11]
- `project_knowledge.py`:
  - docstring :27-31; `ASKED`; `_row`; `_derive_keys` (rows with scope+compare);
  - `_usable` (element rule; markers stay out); `_form`; `_asked_rows`; `_heads` / `_head` (new); `_latest` deleted;
  - `_blank` (+`conflicts`, `condition`); `state`; `_account_state`; `value`; `subjects`; `lessons`; `roster` (precedence through
    `_head`, `conflicts` output); `fact` (new); `holds_none` (new);
  - `record_problems` (keyword-only `rows`, `supersedes`, `condition`, `keys`; marker rules; element rule; role rules only for
    `role_form`); `record` (`condition`, `supersedes`, marker idempotence; lesson words kept); `cmd_revoke` non-role sentence.
  - `notice_from_handoff` is NOT changed (F3 a; N-q3).
- `references/config-keys.json`: the three rows of §2 after :711. The `about` text at :2: "`ask_when` (null, or `first_need` on a row the
  driver asks through the seam)", "for a registry key `scope` and `compare`, and optionally `value` (`one` | `list`, default `list`) and
  `holds` (`none`)" [F-A11].
- `design/state-exits.md` section :155-164: in :157, "the latest valid row ... is in force" becomes the heads rule, with conflict as a
  computed state that exits by a superseding answer or `revoke`; in :161, the lesson/side sentence becomes "revoking the newest row brings
  no older row back"; one new row for the `asked` marker (entered by `Driver.knowledge_asked` for a `first_need` fact; asks nothing by
  itself; out by a later answer, `revoke`, or a newer head; proven by `test_project_knowledge.py`).
- Tests, `test_project_knowledge.py`:
  - `test_fact_toward_asking`: one parameterised set over §3's adversarial inputs (id = the input).
  - `test_fact_steps`: known / not_needed / asked_here / asked_before / unknown / list-key-without-element, each from a minimal
    registry.
  - `test_condition_carried` (PK2-1): a row with a condition reaches `state`, `value`, `fact` and roster entries with it; a row without
    one is unchanged.
  - `test_heads_table` (PK2-2), one parameterised table: a link gives one head; MISSING supersedes every head; a writer names a stale head
    -> a conflict, both heads listed [F-A7 replaces the thread row]; revoke the head -> `unknown` for a role, a side and a lesson (F2 a);
    revoke during a conflict; legacy rows later-wins; a legacy row after a phase-2 row is the head; a cycle and a self-link -> `unknown` +
    problem; a marker is never a head and `roster` / `subjects` / `lessons` skip it; a corrected lesson (new words) is a new row [F-A1].
  - `test_one_value_and_marker_rows`: element `""` accepted for a `value: one` key and refused with an element; role rules not applied
    to it; a marker accepted for a `first_need` key, refused for `product.roles`, idempotent within one story.
  - `test_holds_none`: all `none` -> True; one key without it, an unknown key, an empty list, or a damaged catalogue -> False.
  - `test_catalogue_seam_join` (data join): every `first_need` row carries `scope`, `compare`, `value: one`, `holds: none`, a
    `config:` store, and a `needed_by` entry that names `driver_stage_s6.py:walk_supply_raise`.
- EXPECTED test edits (named, not a STOP) [F-A11]:
  - `test_project_knowledge.py:995-1004`: KEYS = the six plus `manual.accounts_way`, `manual.data_way`, `manual.data_way.may`, in that
    order, each `{"scope": "project", "compare": "exact"}`; the assertion at :1003 over registry stores stays as it is.
  - `test_project_knowledge.py:1007-1012`: the key list inside the text now names nine keys.
  - E44 :876-884: revoking PK-3 prints "no longer read" and "no older answer comes back"; the subject `indexing` is GONE from `lessons`
    (it is not read again); the loop over PK-2/PK-1 then finds them already superseded (each revoke still succeeds; `Indexing` stays).
  - `test_config_migration.py:405-407` (R1): "every row carries a reader list, and `ask_when` is null or `first_need`; a `first_need` row
    carries `scope`, `value: one` and `holds: none`".
  - `test_asked_row_is_skipped` (:267-275) must stay green; if it turns red, STOP.
- given: this spec; P\design\factory-rules.md; plans\builder-rules.md; P\design\architecture.md (AR-13, AR-22, AR-25, AR-28); the
  review §FIX LIST F-A1, F-A2, F-A7, F-A11, F-B1, F-B2.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py` (the functions listed above),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json` (`about` text and three `knowledge` rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (section :155-164),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_config_migration.py` (R1 row :405-407 only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k1.md`
- edges: §4 rows on legacy rows, cycles, links, revoke, markers, conditions, placeholder, damaged catalogue, "K1 merged alone".
- non-goals: the driver; `remember`/kinds (K2); PK2-18 (N-q3); PK2-12 (F14); the FK-4 lift.
- live-runs row (F-B4): "a person takes back a corrected stand lesson through the conductor: the older lesson is not shown again, and the
  conductor's line says the factory asks again".
- depends on: OF3-1 node f merged (F10 a).

### K2 — project kinds, contents, the conductor's door (plan 2.5, 2.6; C2) [F-A8] [F-A9] [F-B8]
- `project_knowledge.py`:
  - new: `KNOWLEDGE_REL`, `kinds`, `kind_problems`, `record_kind`, `contents`, `_keys_for`, `remember`, `cmd_kind`, `cmd_remember`;
  - `cmd_show` gains `--contents`; `main` gains the two parsers;
  - `_usable` / `_form` / `record_problems` / `subjects` take the dynamic keys (F-A8 f);
  - `cmd_remember` / `cmd_kind` start with `_write_prologue` (:844-856) and so `_context` (:817-837) [F-B8].
- `references/install-paths.json`: the rule `{"glob": "qa-factory/knowledge.json", "class": "carried", "reader": "project_knowledge.py",
  "note": "the kinds of knowledge a project defined itself (plan 2.6), with the person's words: committed, carried byte for byte"}`,
  placed after the `config.json` row (:32).
- `scripts/tests/fixtures/judgment-census.json`: rows `kind_problems` (`shape`, owner data, roles `["conductor"]`) and `remember`
  (`xref`, owner data, roles `["conductor"]`), only as the census asks for them. A census demand for any ceilinged class is a STOP (R-1).
- Tests, `test_project_knowledge.py`:
  - FIRST, red-first, the C2 row `test_remembered_fact_survives_restore`: open a story window (take the `restore_config` snapshot as the
    story start does); `remember` `manual.data_way.may` = `"only use what exists"`; run `config_contract.restore_config`; the value is
    still in `config.json` and the DD receipt exists. In the same world, a hand edit of another pointer is reverted (the contrast row).
  - `test_remember_roads`, one table:
    - a config key with a scalar value; an object value merges (a hand-added key survives);
    - two keys in one call reuse a legacy open two-pointer DD row;
    - `--not-needed` on a config key -> a registry row, config bytes unchanged;
    - `--condition-file` on a scoped config key -> a `known` row with the condition; on an unscoped key -> refused before any write;
    - each of the six dedicated-door keys -> refused, naming its door;
    - `--scope story` -> the waiver door; a scope mismatch -> refused;
    - a stand not found or twinned -> refused;
    - a values file empty, not JSON, a list, `{}`, or with an unknown key -> exit 2, nothing written;
    - resolve OK and the registry refused -> exit 2 and the line;
    - `no_trace` -> refused;
    - empty words -> the `person_words.door` text;
    - a `project:<kind>` element added;
    - `--supersedes` naming a stale head -> a conflict.
  - `test_kinds_and_contents`, one table: absent file; unreadable file; twin name by case; empty `says`; a scope change with live elements
    refused; a changed `says` keeps the old object in `history`; an element added and revoked; a list never closed (a new element is
    added, never replaces); `contents()` with no kinds gives the line; `project:<x>` unknown -> refused.
  - `test_install_paths.py` (CI): one row "`qa-factory/knowledge.json` is carried, and its reader exists".
- given: this spec; factory-rules.md; builder-rules.md; architecture.md (AR-3, AR-14, AR-23, AR-24); the review F-A8, F-A9, F-B8.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py` (the functions listed above),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json` (one rule),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py` (one row),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (two rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k2.md`
- edges: §4 rows on knowledge.json, kinds and `remember`.
- non-goals: the conductor's text (K4); the guard (K6); contents in briefs (phase 5); the stand `not_needed`.
- depends on: K1.

### K3 — the seam's bookkeeping in the driver (plan 2.1/2.3; C7, C8, C9) [F-A2] [F-A5] [F-A10] [F-B3] [F-B6]
- `driver_core.Person.__init__` (:202-233) gains two formal attributes, with comments in the style of :208-233:
  - `self.fact_keys = ()`: the catalogue keys this question asks about, set by the raise site's builder and read by `deferrable`;
  - `self.no_hold = False`: the question holds no case, read with `fact_keys` by `deferrable`.
  `offered` is NOT touched: its "set by `no_move` ALONE" invariant (:210-212) holds, because no seam code sets it [F-A5].
- `driver_dispatch.py` — home driver_dispatch, the layer of `say_once` (driver-layers.json:974), so no upward edge [F-A5]:
  - new `Driver.need_fact(self, facts: dict, *, stage: str) -> dict`. `facts` maps a catalogue key to the caller's own `known` bool.
    It returns `{"seam", "ask", "keys", "earlier", "problem"}` and never raises (an exception gives `seam: False` with the problem).
    1. A key without a catalogue row, without `ask_when: "first_need"`, or with a `scope` other than `project` -> `seam: False`, `ask`
       True, `keys` `[]`, `earlier` "". The caller keeps its own road unchanged.
    2. For each key: `PK.fact(self.project, key, story=self.task, known=facts[key])`.
    3. Any key `asked_here` -> `ask: False` (FR-7: once per story).
    4. Keys whose step is `known` or `not_needed` drop out; `keys` = the keys left (`unknown` / `asked_before`); `ask` = `keys` is
       non-empty.
    5. `earlier`, joined by a blank line, in this order:
       - a conflict on a key left -> "Earlier answers about this disagree: <date> (<story>): \"<words>\"; <date> (<story>):
         \"<words>\".";
       - the newest `asked_before` marker among the keys left -> "I asked this in <story> on <date> and got no answer then."
       The words are cut at 160 characters with " ..." (the store keeps them whole). No path or key appears in the text
       (human-questions rule 5). Wording: owner question Q2.
  - new `Driver.knowledge_asked(self, keys, *, stage: str) -> None`. For each key: `PK.record(self.project, key=key, environment="",
    element="", state=PK.ASKED, scope="project", value=None, words="", source="factory", story=self.task, by="driver", where=stage,
    task_root=self.task_root)`. A refusal or an exception is ONE `say_once("knowledge_asked", "note: the factory could not note in the
    project's record that it asked about <keys> (<reason>); a later story will not say it asked before")`. It never raises.
- `driver_dialog.deferrable` first line (:456). POSITION: still the first line, before the holds test. INVARIANT: a gate or exit-4
  Person is never deferred by it, and a doubt asks at once.
  `if getattr(person, "no_hold", False) and (person.kind in ("walk_supply", "data_change") or (getattr(person, "fact_keys", ())
  and person.kind not in GATE_KINDS and person.code != EXIT_GAVE_UP and PK.holds_none(person.fact_keys))): return True`
  (`import project_knowledge as PK` lazily inside the method). The docstring :453-455 says so. The tuple stays until K5 (TEMPORAL).
- `scripts/tests/fixtures/driver-layers.json` [F-B6]:
  - method rows `Driver.need_fact` and `Driver.knowledge_asked` (home `driver_dispatch`);
  - DELETE the ad-hoc row :1118 (`no_hold` is now formal; `test_driver_layers.py:899-901` would report it "used nowhere");
  - any L3 row `test_driver_layers.py` names for the two formal attributes (the builder adds exactly what its L-lines ask and lists
    them).
- Tests, `test_walk_supply.py` (fast, gate_named) [F-B3]: one table function `need_fact_rows` on the `Rig` driver (:29-74) and a real
  project registry. Its rows:
  - no registry -> ask, `earlier` "";
  - the caller's `known` True -> no ask;
  - a `not_needed` head -> no ask; a conditional `not_needed` -> ask;
  - a marker of another story -> ask with the asked-earlier line; a marker of this story -> `ask: False`;
  - a conflict -> ask with the disagree line naming both;
  - a key without `first_need` (a catalogue copy) -> `seam: False`;
  - `knowledge_asked` in a no_trace story -> no registry row, one note, no raise;
  - `deferrable`: `fact_keys` with `holds: none` -> True; the same on a `gate_A` Person -> False; `fact_keys` whose row lacks
    `holds` -> False.
  Existing rows :86-120 stay green unchanged.
- given: this spec; factory-rules.md; builder-rules.md; architecture.md (AR-1, AR-17, AR-20); the review F-A5, F-B3, F-B6.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_core.py` (`Person.__init__` only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`need_fact`, `knowledge_asked` — new methods only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dialog.py` (`deferrable` first line and docstring),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (rows named above),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_walk_supply.py` (one table function),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k3.md`
- edges: §4 rows on markers, the refused write, a damaged catalogue, `no_hold` misuse, "K3 merged, K5 not".
- non-goals: the generic `knowledge` Person, `take_answer`, `ask()`, price keys, F4 tokens (phase 3, Q-2); `driver_machine.py`;
  stand-scoped seam facts (phase 3).
- No live-runs row: nothing a person sees changes until K5.
- depends on: K1. Runs in parallel with K2 (no shared file).

### K4 — the conductor's door in its row (plan 2.4, 2.5; В3) [F-A10]
- `references/conductor-actions.json` `actions`, two edits:
  - one new row (no `id`, like its siblings :26-30), placed after :29. `says`: "the person says, in their own words, that something
    holds for the project or for a stand from now on (a setting, an element of a list the project keeps, or `remember this`)". `run`:
    "project_knowledge.py remember --task <T> (--values-file <file holding {catalogue key: value}> | --not-needed --key <key> | --key
    project:<kind> --element <name>) [--stand <name>] --scope project|stand [--condition-file <file>] [--supersedes PK-<n>] --words-file
    <file>; a kind the project does not have yet: project_knowledge.py kind --task <T> --name <name> --says-file <file> --scope
    project|stand --words-file <file>. YOU decide the scope from their words; on doubt, the narrower one; this story only is a waiver,
    not this command. Then say ONE line: `recorded as a rule of <the project|stand X>: <their words>; to undo, say so`. A role, account,
    side or lesson has its own command above. Never edit qa-factory/config.json by hand for a lasting fact: the story's end gives an
    unrecorded write back. A disagreement the command reports is settled by asking the person, never by picking". This is the В3 rule
    plus F5 (a), placed here because conductor.md has 3 bytes of room (F-17) [F-A10 ii].
  - the revoke row :30 gains the clause "; no older answer comes back by itself — the factory asks again" (F2 a / Q3 a).
  conductor.md is NOT touched.
- Tests, `test_project_knowledge.py`: `test_conductor_row_matches_the_cli` (data join). Every `--option` the new row names after
  `project_knowledge.py remember` / `kind` is an option of that subparser in `main()`, and every required option of those subparsers is
  named in the row.
- Cost (rule 10 a): the row adds about 900 bytes to conductor-actions.json (26999 bytes, read on every conductor call; review key 8).
  The conductor pays it on every call.
- given: this spec; builder-rules.md; architecture.md (AR-17, AR-29); `references/conductor-actions.json` :20-40.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor-actions.json` (one new row; row :30 one clause),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py` (one row),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k4.md`
- edges: the TEMPORAL window K4 before K5: TR3-10 free answers stay on the rows :37-39 (`project_decisions.py resolve --id <DD-n>`);
  `remember` with the same pointers would reuse the same open row, so the two cannot diverge.
- non-goals: conductor.md; the TR3-10 rows :37-39 (unchanged); a price key.
- live-runs row (F-B4): "the person tells the conductor in free words that something holds for the project: the conductor runs
  `remember` with a scope it chose, says the one line, and a later story reads the setting".
- depends on: K2.

### K5 — TR3-10 on the seam (В4; AR-1, AR-15) [F-A3] [F-A4] [F-B3]
- `driver_stage_s6.walk_supply_raise` (:1445-1464). The triggers of :1453 and :1458 are UNCHANGED.
  - way question: `way` = `{"manual.accounts_way": accounts.known}` when `short and not accounts.known`, plus `{"manual.data_way":
    data.known}` when `kinds and not data.known`. When `way` is non-empty and `not self.walk_asked("walk_supply")`: `plan =
    self.need_fact(way, stage="S6")`. If `plan["seam"]` and not `plan["ask"]`, the way question is skipped and the code falls through
    to the data-change check. Otherwise `walk_ask_once` runs exactly as today, with text
    `self.walk_supply_text(short, earlier=plan["earlier"])` and builder `self.walk_supply_person(row, short, fact_keys=tuple(way))`.
    When it returns a Person and `plan["seam"]`, call `self.knowledge_asked(plan["keys"], stage="S6")`, then return the Person.
  - data-change question: the same with `{"manual.data_way.may": data.may_known}`, `data_change_text(kinds, may_change,
    earlier=...)` and `data_change_person(row, kinds, may_change, fact_keys=("manual.data_way.may",))`.
  - `walk_asked` and `walk_ask_once` STAY: they are the in-story guard [F-A4] and the DD-row road shared with `walk_account_raise`
    (:123) [F-A3 b].
- `driver_dispatch.py`:
  - `walk_supply_text(self, short, earlier="")` and `data_change_text(self, kinds, may_change=True, earlier="")`: a non-empty
    `earlier` is the FIRST paragraph of the lead, followed by a blank line;
  - `walk_supply_person(self, row_id, short, fact_keys=())` and `data_change_person(self, row_id, kinds, may_change=True, fact_keys=())`
    set `person.fact_keys`;
  - executors `_answer_walk_supply` / `_answer_data_change` and `_resolve_decision_row` are UNCHANGED (the recorded writer, C2) [F-A3 c].
- `driver_dialog.deferrable`: delete `person.kind in ("walk_supply", "data_change") or` and the tuple sentence of the docstring.
- `design/state-exits.md:204-205`, in "how it is entered": "and, for each fact still unknown (`need_fact`), an `asked` marker in the
  project's registry (refused in a story that leaves no trace: one note)". In "the way out": "the next story's question starts with the
  line that it was asked before and got no answer; a person's recorded `not needed` for the fact stops the question".
- Tests, `test_walk_supply.py` (new rows; existing rows stay):
  - `seam_rows`, one table:
    - asked and unanswered in story 1 -> story 2 asks, the text starts with the asked-earlier line, passes `human_text.problems`
      (`text_of`), and its body hash differs from story 1's (FR-7);
    - accounts known, data unknown -> the way question is asked and only `manual.data_way` is marked [F-A3 a];
    - a registry `not_needed` for `manual.data_way.may` -> no data-change question;
    - a no_trace story with two S6 entries -> one deferred item and no registry row [F-A4];
    - an open legacy two-pointer DD row -> reused (the existing row `open_row_reused_no_second_row` :633 still green);
    - a story in flight holding `walk_supply_asked` -> answered by the same executor [F-A3 d];
    - `deferrable` after the tuple is gone: a builder Person -> True; a `walk_supply` Person with `fact_keys` cleared -> False.
  - `walk_account` is unaffected: its file `test_walk_account.py` is printed by `--witness-for`, and no edit is expected.
- given: this spec; factory-rules.md; builder-rules.md; architecture.md (AR-1, AR-15, AR-16); the review F-A3, F-A4.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s6.py` (`walk_supply_raise` only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`walk_supply_text`, `walk_supply_person`,
  `data_change_text`, `data_change_person`),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dialog.py` (`deferrable` first line and docstring),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (rows :204-205),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_walk_supply.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k5.md`
- edges: §4 rows on the refused marker write, two facts, walk_account, the legacy DD row, stories in flight, "K5 merged".
- non-goals: `walk_account` (Q-1); the executors; conductor-actions.json; driver-layers.json (no new method or state key).
- live-runs row (F-B4): "two stories on one project: story 1 leaves the way question unanswered; story 2 asks it with the line that it
  was asked before; after an answer, story 3 does not ask".
- depends on: K3. Runs in parallel with K4 (no shared file).

### K6 — guard: approvals and the new write commands (B-294 (a); "писатель фактов один") [F-A6]
- `guard_pre_tool.human_word_check` (:1758-1803), three changes in the shape of :1784-1797:
  - the regex :1789 gains `remember|kind` (`(?:account|role|revoke|side|lesson|remember|kind)(?![\w-])`);
  - a new alternative for `config_contract.py` with any abbreviation argparse resolves to `--record-approval` or `--apply`
    (allow_abbrev; F-21): `config_contract\.py` followed, anywhere in the exec part, by `--re(?:c(?:o(?:r(?:d(?:-(?:a(?:p(?:p(?:r(?:o(?:v(?:a(?:l)?)?)?)?)?)?)?)?)?)?)?)?)?(?=[\s=]|$)`
    or `--appl(?:y)?(?=[\s=]|$)`;
  - the same for `onboard_apply.py` with `--appl(?:y)?(?=[\s=]|$)`.
  INVARIANT: the read and plan options stay open (`--migration-plan`, `--validate`, `--check-environment`, `--answers`,
  `--price-table-answer`, `--preflight`, `--listing`, `--proposal`, `--approval-ref` alone), and the main session is never refused
  (F-22).
- `HUMAN_WORD_MSG` (:1726-1755):
  - :1740-1742 becomes "`project_knowledge.py account`, `role`, `revoke`, `remember` and `kind` store what the person said (the product's
    roles, the stand's accounts, a lasting setting, a kind of knowledge the project keeps), or take it back; a role running them would
    turn its own inference into a project fact (`show` and `lessons` are open to you)";
  - plus one sentence: "`config_contract.py --record-approval` / `--apply` and `onboard_apply.py --apply` record and apply what the person
    approved at onboarding; a role running them would approve its own configuration (`--migration-plan`, `--validate` and `--preflight`
    are open to you)".
- `_SANCTIONED_CONFIG_SCRIPTS` and its pin (`test_guard_write_owners.py:815-817`) are NOT changed.
- Before the edit, the builder greps `--record-approval|config_contract\.py --apply|onboard_apply\.py --apply` over `P/agents`,
  `P/skills` (phases included) with a positive control (the same grep finds `config_contract.py:2980` when run over `P/scripts`). A
  hit in a ROLE's text is a STOP; a skill run by the main session is fine.
- Tests:
  - `test_guard_project_knowledge.py` table rows: `remember` and `kind` refused to a role; `show --contents` and `lessons` pass.
  - `test_guard_write_owners.py` (CI) table rows: a role is refused `config_contract.py --root . --record-approval p.json`,
    `--record p.json`, `--re=p.json`, `--apply p.json` and `--appl p.json`, and `onboard_apply.py --root . --apply`; a role passes
    `config_contract.py --root . --migration-plan`, `--validate` and `--approval-ref x`, and `onboard_apply.py --preflight`; the main
    session passes `--record-approval`.
- given: this spec; factory-rules.md (A, C FR-39); builder-rules.md; architecture.md (AR-9, AR-14); the review F-A6.
- owns:
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\guard_pre_tool.py` (`HUMAN_WORD_MSG`, `human_word_check` only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_guard_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_guard_write_owners.py` (new rows only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k6.md`
- edges: abbreviations and the `=value` form (above); a quoted call inside a heredoc stays unmatched (the exec-part rule, :1763-1765);
  the commands named before K2 merges cost nothing.
- non-goals: the sanction table; B-294 (c) (F6 a); PK2-9's subcommand-anywhere form (queued after K6).
- live-runs row (F-B4): "a full story on the stand: no role is refused by the person's-word guard while doing its normal work (guard
  log)".
- depends on: nothing. Queue: `очередь: OF3-2/K6 → project-knowledge/2 PK2-9` (same file).

### K7 — the map axis "memory of a person's answer" (§7 C3)
- `docs/SIBLING_MAP.md`: axis 37. Survivor: `project_knowledge` (`fact` / `record` / `remember`, the `asked` marker). Twins, each with its
  phase or "stays — why":
  - `environment_record` (`accept always`, until phase 3.2);
  - `stand_identity` (phase 3.2);
  - stand lessons (`environments.stand_lessons`, SS1-11: already in the registry);
  - TR3-10's open DD row reused across stories (`walk_ask_once`, stays as the config write's receipt);
  - `walk_account` (Q-1);
  - onboarding's remembered answers and `asked_until_answered` (phase 4);
  - report adaptations RA-n; `waiver --carry-from`; `obligations.md`;
  - the confirmed default stand;
  - the driver's in-story hash memory (`already_answered`, stays by design, C7).
  UNVERIFIED carrier names: the builder greps each name with a positive control and reports any it cannot find, never inventing one.
- Doc-dispatch witness (CLAUDE.md rule 11): a key-presence script with the keys quoted from this item before the run, its full source in
  the report, and a negative control.
- owns: `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md`
- depends on: nothing; parallel.

### Order and parallel groups
- G1 (start): K1 (after OF3-1 f), K6 and K7, in parallel.
- G2: K2 ‖ K3 (both after K1).
- G3: K4 (after K2) ‖ K5 (after K3).
- Serial files: `project_knowledge.py` and `test_project_knowledge.py` go K1 -> K2 -> K4; `driver_dialog.py` and `driver_dispatch.py`
  go K3 -> K5 (different functions); `test_walk_supply.py` goes K3 -> K5; `state-exits.md` goes K1 -> K5 (different sections);
  `guard_pre_tool.py` is K6 only.
- At most 3 writers at once.

edges: §4. non-goals: «Not in this phase» below. handoff: builder report + diff + the census of every new reader/writer site.
siblings:
- axis 34 (one road: the tuple folded, K5; `remember` vs the doors, K2; one revoke rule, K1; walk_account residual, Q-1);
- axis 5 (only the S6 consumers in phase 2);
- axis 13/16 (one reader, one precedence);
- axis 35 (side keys stay `known`-only; their revoke follows the heads rule);
- new axis 37 (K7).

### Mapping: every plan sub-item and §7 correction -> a node or "not in this phase"

| item | where |
|---|---|
| 2.1 `need()` with the order of §2.3 | K1 (`fact`, pure) + K3 (`need_fact`, bookkeeping) |
| 2.1 state of a fact in the registry | K1, on the phase-0 registry (C1) |
| 2.2 B-296 | not in this phase — dropped by C1 (stale after HF8-9) |
| 2.3 question carries the fact key; "already answered" by key | K3 (`Person.fact_keys`; cross-story memory via markers); the in-story hash and `walk_asked` stay (C7) |
| 2.4 scope variants | the conductor's scope (K4); the closed tokens are phase 3 (Lead decision on Q1 = (a)); revoke (K1) |
| 2.5 conductor's "remember" door | K2 (`remember`), K4 (row) |
| 2.6 lists, project kinds, contents, install-paths | K2 |
| Absorbs TR3-10 | K5 (the way and data-change questions); `walk_account` -> Q-1 |
| Absorbs B-294 | K6 for (a) and the role side of (b); (c) phase 4 (F6 a) |
| Absorbs the release-next finding | roles: guard (t-110) + K6; conductor: K4 row + F5 (a) |
| PK2-1 | K1 (`condition`) |
| PK2-2 | K1 (`supersedes`, heads, conflict, revoke) |
| PK2-18 | N-q3 (F3 a), restated against heads |
| C1 / C2 / C3 / C5 | K1 / K2 first test / K7 / §2 |
| C7 | K3/K5 (cross-story markers; in-story guards kept) |
| C8 | K3 (deferral by catalogue) + K5 (tuple removed) |
| C9 | K1 (`fact` pure) / K3 (the driver writes markers) |
| C10 | phase 3 with `while_unknown` (no phase-2 consumer, F-B5); `unreachable` not stored |
| C13 / В8 | the `noticed_unconfirmed` state (phase 0); role-side wiring phase 5.1а |
| C14 | writers closed by `_refuse_no_trace` (K1/K2); per-arm snapshot N-q2 |
| plan witness "tests per state and per `while_unknown`" | K1 `test_fact_steps` + `test_fact_toward_asking`; `while_unknown` rows come with the field (phase 3) |

**Not in this phase:**
- phases 3-6;
- phase 1 part f;
- `derive` (F8); `while_unknown`, `safe_direction`, `question`, `answer`, `person_class`;
- the generic knowledge Person and the F4 tokens (Q-2); the "acting on your answer" line; the FK-4 lift;
- kinds' `needed_by` and the role filter of `contents`;
- `accept always` onto the registry (3.2); `walk_account` (Q-1);
- PK2-11/PK2-19 (the no_trace class); PK2-12/PK2-13 (helpers; F14); PK2-9 (after K6).

## §6 Forks

Lead decisions of round 1, applied as written: F1 (a), F2 (a), F3 (a), F5 (a), F6 (a), F7 (a), F8 (a), F9 (a), F10 (a), F11 (a).

Where a review fix touched a Lead decision, without changing its meaning:
- F2 (a) now also covers lessons and sides, and roles (whose code revived the previous row while their sentence said "asked again",
  F-6b). The owner question is Q3.
- F5 (a)'s conductor rule moves from conductor.md into the conductor-actions row (byte cap, F-17).
- F7 (a) works only because markers are outside heads (F-A2 i); folded.
- F9 (a) takes two `known` inputs for walk_supply; folded.
No Lead decision is contradicted by the current code. Nothing is flipped.

F4 — Lead decision (review Q1 = (a)): phase 2 adds no "not needed now / for this stand / for the project" tokens. The two walker
questions keep their own answers. F4 waits for phase 3 with the first generic knowledge question (queue Q-2), where the owner decides
its words.

| id | question | options and cost | recommendation | whose |
|---|---|---|---|---|
| F12a | Stored shape of `supersedes` on projects' disks [F-A2 ii] | (a) a LIST of ids (`[]` = read none); one answer can settle a conflict of two heads. (b) one id or null; settling a two-head conflict takes two `remember` runs, i.e. two rows of the same answer | (a) | Lead (stored format) |
| F12b | Element of a one-value key's rows [F-A2 iii] | (a) `""` (no element: honest, and the registry already compares elements exactly). (b) a fixed `"-"`; cost: a sentinel every reader must know | (a) | Lead (stored format) |
| F12c | `provenance.source` of an `asked` marker | (a) a new word `factory` (accepted only with state `asked`). (b) `role`; cost: it reads as if a role said something | (a) | Lead (stored format) |
| F12d | Key namespace for project kinds in the carried registry | (a) `project:<name>` with the name rules of §3 (case-folded unique, 1-60 chars). (b) a separate key field `kind`; cost: a second key column every reader joins | (a) | Lead (stored format; renaming later means migrating rows) |
| F12e | Changing a kind's `says` in the committed `knowledge.json` | (a) the whole previous kind object appended to `history`. (b) refuse a change (a new name instead); cost: a typo fixed means a new kind and moved elements | (a) | Lead (stored format) |
| F14 | Order against project-knowledge batch 2 [F-B7] | (a) K1 before PK2-12; PK2-12's row gets the line "one precedence = `_heads` (supersedes-aware); `ER.covering` keeps later-wins for the environment record, or gains heads — decide at PK2-12". (b) PK2-12 first; cost: K1 rebases onto a merged later-wins helper and replaces it again. K6 before PK2-9 stays as round 1 queued it | (a) | Lead (order against another stream) |

Owner questions (plain words, options). The nodes run on (a) until the owner answers:
- **Q2 (texts you will read).** The wording of four lines:
  1. After the conductor records your free answer, it says one line, e.g. "recorded as a rule of the project: <your words>; to undo, say
     so".
  2. A walker question asked again in a later story starts with "I asked this in <story> on <date> and got no answer then."
  3. If two of your recorded answers about it disagree, the question starts with "Earlier answers about this disagree: <date> (<story>):
     "<words>"; <date> (<story>): "<words>"."
  4. When you take back a side or a lesson, the line says "no older answer comes back; the factory asks again".
  Options: (a) yes, these wordings; (b) change them (give your words).
- **Q3 (taking back an answer).** Today, if you correct a stand lesson (or a side) and then take the correction back, the older one comes
  back by itself. The new rule for every answer: taking back does not bring the older one back, and the factory asks again.
  - (a) The same rule for lessons and sides. Recommended: one rule everywhere.
  - (b) Lessons and sides keep bringing the older one back; cost: two revoke rules in one registry (P31 needs the owner's word for
    that).

## §7 Queue entries and findings (the coordinator places them)

| id | what | owns (prefix P) | test | when |
|---|---|---|---|---|
| N-q1 | F5 (a) detector: `restore_config`'s reverted pointers of a story reach the report as one finding line naming `remember` | P\scripts\config_contract.py (`restore_config` caller side) or the report writer | a hand-edited pointer reverted -> the line; a recorded write kept -> no line | after K4; after OF1-2 |
| N-q2 | C14 per-arm knowledge snapshot for comparison runs (P8) | `docs/RUNBOOK.md` §9 + `experiments/measurers/run_headless.py` | a doc key-presence run or a measurer test | before the next comparison run |
| N-q3 | PK2-18 (F3 a), restated: "write `noticed` only when the subject has no head or its single head is `noticed_unconfirmed`" | P\scripts\project_knowledge.py (`record`, `notice_from_handoff`) | the finding's row | right after K1 |
| Q-1 | `walk_account` onto the seam: its fact is `environments.credentials_by_role` (stand scope, the account door); marker + earlier line; P31 residual of F-A3 b | P\scripts\driver_stage_s6.py (`walk_account_raise`), P\scripts\driver_dispatch.py (`walk_account_text`) | `test_walk_account.py` row: asked and unanswered in story 1 -> story 2 asks with the earlier line | phase 3 (stand-scoped seam facts); owner: Lead of onboarding-forge batch 3 |
| Q-2 | the generic knowledge question: Person kind, `take_answer` branch, F4 tokens (owner), `knowledge.first_need`, fields `question`/`answer`/`person_class`/`while_unknown`/`safe_direction` | P\scripts\driver_*.py, P\references\question-prices.json, config-keys.json | the phase-3 node's rows | phase 3.1, with the first gate-A key |
| PK2-12 line | F14 (a): add the line to `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md:33` | — | — | with K1's dispatch |

Announcement: `очередь: onboarding-forge/3 OF3-2/K6 → project-knowledge/2 PK2-9` and `очередь: onboarding-forge/3 OF3-2/K1 →
project-knowledge/2 PK2-12` in both batch files (F14 a). The stream owners of the driver set are told that K3/K5 touch `driver_core.py`,
`driver_dialog.py`, `driver_dispatch.py` and `driver_stage_s6.py` (functions listed).

## Plan text vs section 7 (and vs the repo) — for the Lead to correct stale rows

| where | stale text | the later word / the fact | carrier |
|---|---|---|---|
| plan §4 2.1; batch-3 OF3-2 row | "`project_decisions.upsert / resolve` обобщаются" | C1: the registry is built on `environment_record` helpers (phase 0); `project_decisions` stays the deferred-decisions registry and the recorded config writer | plan :330; project_knowledge.py:1-6 |
| plan §4 2.2 | "B-296: реестр умеет указатель на элемент списка" | C1: dropped | plan :330 |
| plan §2.1, §2.6, §6 | `references/project-knowledge.json` (new table) | C5: section `knowledge` of `config-keys.json` | plan :338 |
| plan §2.1 table fields `question`, `answer`, `person_class`, `while_unknown`, `derive` | all in phase 2 | phase 3 / 4.2 when their first consumer lands (F-A10, AR-22); `about` = `scope` | this spec §2 |
| plan §2.1 ratchet "у строки `first_need` есть ... текст вопроса" | the question text named on the row | in phase 2 the three `first_need` rows' texts live in their builders (`s6.*` price keys); the row field comes with Q-2 | driver_dispatch.py:3260, :3383 |
| plan §2.3 | one `need(key, env, story)` that reads and asks | C9: pure `fact()` + the driver's `need_fact` / `knowledge_asked` | plan :339 |
| plan §2.3 p.4 | a stop-bound question mechanism "t-1957 §3.6 п.3" | C8: TR3-10 built it for two kinds (driver_dialog.py:456); K3/K5 put it on the catalogue | plan :340 |
| plan §4 2.4 | tokens "только сейчас / для стенда / для проекта" in phase 2 | Lead decision on Q1 (a): phase 3 (Q-2) | review Q1 |
| plan §4 2.x witness | "тесты ... каждого `while_unknown`" | phase 3 with the field | this spec §2 |
| plan §2.1 / §2.2 states | `in_turn`; `unreachable` stored | C10 | plan :343 |
| plan §2.4 "проект, всегда -> config.json" | a direct write | C2: only through the recorded writer | plan :331 |
| plan §4 «Поглощает: TR3-10» | as if TR3-10 waits | В4: TR3-10 is «принято» with its own road; K5 moves two of its three questions, Q-1 the third | batch-3-parallelnost.md:31 (round 1) |
| plan §7 C3 | the axis is created by the phase-0 commit | not in SIBLING_MAP (axes 1-36) -> K7 | F-24 |
| B-294 finding line numbers | guard :1359/:1656/:1700 | the role door is `human_word_check` :1758-1803 (regex :1789); the sanction table is not the mechanism | F-21 |
| PK2-12 row :33 | one later-wins precedence | heads (F14) | batch-2 :33 |

## Small choices I closed
- `scope` kept for the plan's `about`. `ASKED = "asked"` outside `STATES`. Helper names `_heads`, `_head`, `_row`, `_keys_for`,
  `holds_none`. The `fact()` step names.
- `value` absent = `list`, so only the three new rows change.
- KEYS entries keep `{scope, compare}`; other fields come through `_row`.
- `project:<kind>` elements follow the side-name form rules.
- `need_fact` lives in driver_dispatch (F-A5). `need_fact` serves project-scoped facts only in phase 2.
- F-A3 (c): the TR3-10 executors keep `_resolve_decision_row` (the recorded writer they already use; refs unchanged, so legacy rows and
  stories in flight need nothing), and they write no registry `known` row: for a config-stored fact the carrier decides and the receipt
  holds the words (AR-22: nothing would read that row). `remember` writes a registry row for a config key only when it carries what the
  receipt cannot (a condition, or `not_needed`).
- `remember` merges object values in code (F-A8 c, the review's choice), takes one `--values-file` object of catalogue keys, and uses
  the `asked` evidence text of §3 step 7 (F-A8 d).
- The conductor's text goes into the conductor-actions row with no `id` (F-A10 ii; its siblings :26-30 have none).
- The earlier and disagree lines cut words at 160 characters.
- `safe_direction`, `while_unknown` and the other unread fields wait for phase 3 (F-B5).
- One changelog fragment per node.

## Contradictions and notes for the Lead (not widened)
- Roles revive today too (F-6b): `cmd_revoke` says "it is asked again where it is needed", but `_latest` reads the previous live row.
  F2 (a) makes the sentence true; no role test is expected to redden (UNVERIFIED: K1's `--witness-for` run will show it — a red role row
  is a STOP).
- `project_decisions` does not read `no_trace` (F-19): today a TR3-10 answer in a comparison run writes the project's config with a
  receipt that survives `restore_config`. This is a P8 sibling of PK2-11/PK2-19, not widened here; it is a finding for that pile.
- `test_conductor_doors.py` and `test_driver_layers.py` are red at quarantine entry, so K3 and K4 report their own row ids from them
  rather than a green file.
- Phase 0's `acting_line` serves gate A accounts only; its generalisation waits for phase 3.

## Trail
Read on read-main this round:
- `P/scripts/project_knowledge.py` :1-1099 (whole except :870-899);
- `P/scripts/driver_stage_s6.py` :85-144, :1425-1504; `P/scripts/driver_dispatch.py` :3225-3424; `P/scripts/driver_dialog.py` :440-469;
  `P/scripts/driver_core.py` :200-239;
- `P/scripts/project_decisions.py` :398-524; `P/scripts/config_contract.py` :2960-3022 (+ grep `walk_supply_keys|accounts_way`);
  `P/scripts/guard_pre_tool.py` :1700-1804; `P/scripts/report_facts.py` :1980-1999, :2165-2204;
- `P/references/conductor-actions.json` :20-41; `P/references/config-keys.json` :1-4, :700-763;
  `P/references/templates/config.json` :60-67; `P/design/state-exits.md` :155-166, :200-206;
- `P/scripts/tests/test_project_knowledge.py` :262-277, :870-889, :990-1015; `P/scripts/tests/test_config_migration.py` :364-415;
  `P/scripts/tests/test_walk_supply.py` :20-123 (+ def list); `P/scripts/tests/test-layers.json` :6579-6608, :7005-7044;
- `plans/project-knowledge-plan.md` :50-69, :218-231 (+ headings grep); `docs/TESTING.md` :36-145; the review whole; this spec whole.
Greps (positive control in brackets):
- driver-layers.json rows [layers :9];
- `def walk_supply_keys|accounts_way` in config_contract.py;
- `closed_by_run|no_trace` in project_decisions.py [project_knowledge.py:558];
- `AWAITING_ITS_SITE|SIZE_CAP|census_problems` in test_conductor_doors.py; conductor-actions in tests;
- test-layers keep names; slow_tests.json [config_migration found]; SLOW_TESTS;
- `PK.KEYS|CATALOGUE_PROBLEM` over scripts; `adhoc` in test_driver_layers.py;
- judgment-census rows [`_refuse_no_trace` :783]; CEILING in test_judgment_census.py;
- `--apply|--record-approval` parsers; `ArgumentParser` in onboard_apply.py;
- PK2 rows in the batch-2 file; OF3 statuses; artifact-writers.json [its `"artifacts"` keys]; install-paths.json;
- `s6.*` price keys; SIBLING_MAP `^## Axis 3[3-9]`; test_words_doors.py `.py` door scan;
- `def person_words_whole|say_once|deferred_items|defer_question`.
Not verified (UNVERIFIED in the text): M-2; F-15; F-20 (review-verified); the 79-row count (review run); the K7 carrier names; whether a
role row reddens under F2 (a); the L3 rows `test_driver_layers.py` will ask for; whether any role text names `config_contract.py --apply`
(K6 greps first).
needed beyond the manifest: everything under `.claude/worktrees/read-main/` listed above (the manifest named the spec, the review, the
plan and TESTING.md).

## Lead decisions on the forks (round 1, Lead, Fable, 13.11.2026 — "решила сама", the owner may overrule)

- F1 (a), F2 (a), F3 (a) (PK2-18 stays its own node right after K1), F5 (a), F6 (a), F7 (a), F8 (a), F9 (a), F10 (a) (K1 waits for
  the phase-1 node f), F11 (a): the designer's recommendations are taken as written.
- F4 is the OWNER's (what a person is shown, P9): open; the nodes run on recommendation (a) until the owner answers.
- State of this draft: accepted by the Lead as a draft; the critic-on-plan pass is review
  `docs/tasks/specs/reviews/of3-2-knowledge-phase2-plan-review.md`. No node of K1-K7 is dispatched before its fix list is folded into this
  file.

Round 2 (Lead, in the t-464 brief): review Q1 -> (a), F4 moves to phase 3; Q2 and Q3 are the owner's, open, and the nodes run on (a);
F1-F3, F5-F11 as above; the F-A10 principle holds. All applied in round 2 (§6).

Round 3 (Lead, Fable, 13.11.2026, after the fix round t-467 — "решила сама", the owner may overrule): F12a (a) `supersedes` is a
list; F12b (a) element `""` for a one-value key; F12c (a) source `factory` for an `asked` marker; F12d (a) `project:<name>`; F12e (a)
the previous kind object goes to `history`; F14 (a) K1 before PK2-12, and the line for PK2-12's row is written by the Lead of the
next session together with the queue line. These are stored formats on projects' disks: they are final at the first release that
carries K1/K2, so an objection is cheap only before K1 is dispatched. Q2 (wording of the new lines) and Q3 (a taken-back lesson does
not revive the older one) stay the OWNER's; the nodes run on (a).

OWNER'S WORD (владелец, 13.11.2026, in the session with the Lead, on the round-3 list): the stored formats F12a-e and the order F14
are OK ("остальное ок"). And a NEW requirement on the `asked` marker: "если ответ нужен не для одной стори, а для проекта, то
показывается на дашборде в отложенных решениях" — an asked-and-unanswered fact whose scope is the PROJECT (not one story) is shown on
the dashboard among the deferred decisions.

Node K8 (new, opened by that word; PROJECT.md "спека, меняющая смысл" item (г): a new owner decision is a new node, it is not folded
into K1 or K3). Direction chosen by the Lead: there is ONE carrier of deferred decisions already — the registry written by
`scripts/project_decisions.py` (table `## Deferred decisions (onboarding/gates)`, HEADING :67; audit A13 in `audit_factory.py`) — so
the `asked` marker of a project-scoped key gets an OPEN row there through `project_decisions`' own upsert (the recorded writer, AR-14;
no second list, P31), carrying the question's text as the person saw it and the story and date it was asked in; recording an answer
for that subject (K1 `record`, K4 `remember`) resolves the row through `project_decisions.resolve`; a story-only fact (no project
scope) never gets a row. STAND-scoped asked markers get a row too (владелец, 13.11.2026: "да" to "отметка про конкретный стенд тоже
должна попадать на дашборд?"); the row names the stand. Open for the designer's short draft before dispatch (UNVERIFIED by the Lead, not read this session): which
reader the dashboard uses for "deferred decisions" and whether it reads that table or another carrier; the no_trace story edge
(§4: a comparison run leaves no trace, P8 — no row). Depends on K1 (the `asked` producer) and K3 (the ask half); critic-on-plan for
K8's draft only (a new idea's node), not a re-review of K1-K7.

STATE: READY FOR DISPATCH by the next session (K1-K7; K8 needs its short draft first) — review t-463 folded (19 fixes, table at the top); the second critic pass is NOT owed
(PROJECT.md step 6: the fix round does not change the architecture; the Lead checked that all 19 fix ids are located in the file).
Items marked UNVERIFIED are checked by the Lead of the dispatching session against main before the node that rests on them goes out
(CLAUDE.md rule 11, checklist item 5). Order: phase-1 node f (ratchets R2/R3) -> K1 -> PK2-18; the groups are in §5.
