# t-1123 — plan critic on card C3-j r2 (stand page load: measured, or deleted)

Reviewed: `docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md` (whole, both "Lead decisions" blocks: F-j0 = (C), route (a),
split (a)), against r1 `docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (§ owner's word :894-900) and the package on
the root checkout `b89871b3` (= origin/main; the card was drafted on `9a7acdf3`; every anchor I cite was re-read on b89871b3).
Critic on plan: no code was written by me; one witness-shaped run (scenario_walk) was attempted, see trail.

**Verdict: READY WITH FIXES** — the direction (C) is sound and honours the owner's two words; no branch asks a person.
But j1 as written cannot be executed inside its `owns` (callers, fixtures, census, test-layers it does not own), it stores a
machine-local failure in a carried, never-retried record, it opens a second store for stand facts beside the answer registry
(P31/AR-14), and its queue contradicts the k-cards r2. All 22 fixes below are executable in one designer/Lead round; none
needs the owner except F-home (K9), which is already routed to her.

---

## K1. §A evidence — HOLDS for the producer, FAILS (incomplete) for the readers

Producer, wait half and load half: holds.
- Grep (shell, case-insensitive, `-rli`) over `ai-packages/qa-factory/` for
  `page_object_max_wait_s|e2e_page_load_s|_e2e_limit|stand_limit|check_s5_stand_limits|measurement_is_stale|limit_seconds|skip_stand_limits`:
  hits only in `design/factory-rules-debt.md`, `references/config-keys.json`, `references/gate-registry.json`,
  `scripts/cost_capture.py` (a different `_limit_seconds`, :3364 — not this concept), `scripts/gate_preflight.py`,
  `scripts/manual_capture.py`, and tests/fixtures. Positive control: same call found `gate_preflight.py` (24 py hits for
  `skip_stand_limits|e2e_stand_limit`).
- No writer: grep for `"measured":`, `['measured']`, `setdefault("measured"` over `scripts/` outside tests → only unrelated
  `measured` keys (friction.py, role_load.py, run_counters.py…); positive control `"measured"` gives 49 py hits.
- No `.md`/template asks onboarding to record it: grep `page_object_max_wait|e2e_page_load|page.load` over `--include=*.md
  --include=*.json` (fixtures excluded) → no onboarding/skill/agent hit; `references/templates/` has neither key.
- `brief_pack.py` carries neither key: absent from the file list of the first grep (same call that found gate_preflight).
- The wait half's only reader is `_e2e_limit` (`gate_preflight.py:3119`); `check_s5_reporter`'s `over` skip :3323-3330 and
  `_stand_limit_card` :3243-3273 read the load: as stated.

Readers of the load half: the card's list is INCOMPLETE. `timeout_for(` callers on b89871b3 (grep over `scripts/` outside
tests):
- `gate_preflight.py:2808` (named), `manual_capture.py:3413` (named), `manual_capture.py:5383` (≈ the ":5430-5445 region" —
  wrong anchor),
- NOT named: `manual_capture.py:3015` (`sign_in`), `manual_capture.py:3178`, **`investigation_probe.py:419`**,
  **`walk_session.py:1221`**.
- And a fixture producer the card missed: `scripts/tests/fixtures/manual-evidence/scaffold.py:68` writes
  `"measured": {"e2e_page_load_s": {"value": 70, ...}}` into the shared manual-evidence config; `test_manual_capture.py:194`
  ("the browser opened with the measured limit (70 + 30)" → 100), :262 ("the limit is 100 s"), :273, :951, :1040, :1558,
  :1660 all lean on it. The card's E12 fixture grep searched for the check id and note text, not for the config key, so it
  missed this.
The "automator, code critic, runner, failure analyst" users are PROPOSED readers, not present ones (the card says so honestly
in §A "one worker today, and one it should have").

## K2. Does any branch ask a person or put a factory reason to a person — HOLDS for j1/j2, one sibling outside

- j1 `check_stand_page_load`: notes only, never `add` (§2 item 2) — no question, nothing blocks. Holds.
- j2 deletes the PERSON_DECIDES `over` card (:3262) and both FACTORY_DEFECT findings with waiver doors (:3197, :3208). Holds.
- Window (j1 merged, j2 not): the old check still runs, unchanged — no NEW asking, but see K5 (contradicting notes).
- BUT j1's texts misattribute owners (FR-19/AR-27, FR-3 "reported", correctly, yet with the wrong owner): every `failed` is
  "a defect of the factory", including a stand with no web address (API-only, device stand: the project's shape, not a
  defect), a stand that does not answer (the stand's), a frontend that redirects to a host outside the stand's hosts (the
  config's), and "no browser on this machine" (the machine's). Fix 5.
- Sibling of the same class (a number a person cannot know, put to a person), outside this card: `check_s5_reporter`'s
  `timed_out` card, `gate_preflight.py:3635-3641`: "answer with your approval: raise `gate_rehearsal.reporter_timeout_s`, or go
  on". After j2 the reporter rehearses every non-handed profile on a slow stand (E14), so this card becomes the reachable
  successor of the deleted `over` skip. Fix 21.

## K3. j1 feasibility and edges — PARTLY HOLDS

Feasible as written: `PlaywrightBackend.goto(url)` exists (`manual_capture.py:1814-1815`, `wait_until="load"`, timeout =
`open`'s `timeout_s`), returns the elapsed seconds through `_timed` (:1801-1812), and raises a DISTINCT `StepTimeout` on the
page-load timeout vs `StepFailed` on any other browser error. The gate already opens this backend at gate A
(`_probe_sign_in` :2803-2811). So the card's "if there is no navigation call, STOP" is resolved: name it (Fix 9).

Edge by edge:
- Stand unreachable (connection refused, DNS): `StepFailed` → `failed` → RECORDED and REUSED ("a failed row is reused like a
  measured one"). Reuse ends only on a new definition sha or a newer `verified` — and `environments[].verified` is written
  once at onboarding (`skills/qa-onboarding/phases/p4-generate.md:291`). So one gate A run while the stand was down disables
  the measurement for that stand indefinitely. Decided WRONG (an unknown made permanent). Fix 3.
- No browser on this machine: `failed` recorded into `qa-factory/records/` — a CARRIED file ("carried by the project: every
  machine that uses it reads the same file", `environment_record.py:5-6`). A colleague's machine WITH a browser then reads
  `failed` and never measures. AR-4 broken (a machine fact written into a project record). Fix 3.
- Load never finishes: `StepTimeout` at CAP_S=180 → `measured, at_least: True, load_s: 180` → `timeout_for` = 210. Decided
  right (FR-41 "at least"), but the card does not state the 210 — state it (Fix 9).
- No frontend (API-only project) / device stand (`surface` row, `stand_identity.py:133-143`): the trigger fires on any
  manual case (`_actors_of_manual_cases` or a `manual-agent` row) even when it is an http-only case, then `frontend_of` →
  `""` → `failed` "a defect of the factory". Decided WRONG: no web page exists, so there is nothing to measure; that is
  `n/a`, not a failure and not the factory's defect. Fix 4.
- Credentials in the address: the card says `frontend_of` refuses them. It does not: `env_probe.frontend_address`
  (:421-427) accepts any `http(s)://` string, userinfo included. As written, `https://user:pass@host` would be stored in
  `address` in a carried record and printed into four roles' briefs. Fix 6.
- Several stand definitions: gate (`_selected_environment` :5139-5146) and brief (`brief_pack._stand_pick` :2734-2745) use
  the same rule (pipeline's name, else the only row), so they agree; two rows sharing one name: the gate takes the first,
  `_stand_pick` returns None, `stand_identity.definition_sha_for` takes the first — the brief would say "not measured yet"
  for a measured stand. Undecided. Fix 7.
- Two gate A runs at once on one project (parallel windows): read-modify-write of one JSON file without a lock; one row can
  be lost. Undecided (benign if stated). Fix 2 resolves it (the registry has a lock, `project_knowledge.py:46`).
- Unreadable record (E7), placeholder stand (E1), staleness (E8), off switch (E9), no use (E10), handed (E11): decided and
  right, subject to Fix 3 on reuse.

## K4. j2 deletion whole (AR-22) — FAILS on four items

Covered: `_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`, `limit_seconds` (readers: :3129, :3135, :3252, selftest
:6394 — all inside the deleted set), `measurement_is_stale` (:195, :3158, :6398), the `run` entry :6089, the reporter skip,
docstrings :57/:804/:3104-3107, registry row, census row :418, `test_gate_registry.py` pins, changelog. The FR-59 debt line
`design/factory-rules-debt.md:111` is legitimately left to its one writer S1b (RD1-23, `batch-1-phase-2.md:51`).
Left:
1. `references/config-keys.json` `needed_by`: `gate_preflight.py:check_s5_stand_limits` (row `profiles`, :724) and
   `gate_preflight.py:_stand_limit_card` (row `environments`, :733). Not machine-checked (grep `needed_by` over tests/tools:
   only `test_config_migration.py:400-407`, which checks the list TYPE), so they rot silently. j1 also adds new readers of
   `environments` that the catalogue must name. Fix 13.
2. The runner list of `test_gate_preflight.py`: it calls tests by name (:6244-6249 call
   `test_the_other_stand_is_named_only_when_its_own_load_fits`, `test_the_stand_limit_step_can_be_switched_off`, …). Deleting
   the functions in :2734-2935 without deleting EVERY runner line that calls one breaks the file with a NameError; the card
   names only :6248 and :6264, and its "every hit of the five words" net misses names without those words. Fix 14.
3. The test helpers `record_edit` (:4072-4077), `with_limits` and the `record` lambda in `scenario_messages` (:3758-3760)
   write the deleted keys; their callers go too. The card names :4070-4120 only as "rows that assert on the card". Fix 14.
4. The finding `plans/piles/rules-debt/findings/20261117-rd2-c3-j-s5-stand-limits-otvet-v-reestre.md` and the batch row
   RD1-13 (`batch-1-phase-2.md:41`) still prescribe r1 (registry answer, `environment_record.py` third scope) and declare
   r1's zone. A weaker executor reading the batch row gets the opposite direction. Fix 16.

## K5. The window and the serial order — FAILS

Window: no moment lacks protection (the old protection never fired: nothing produces its inputs — M5, 3/3). But between j1
and j2, gate A shows TWO contradicting notes in one packet: the old `check_s5_stand_limits` "e2e page load on {stand} is not
measured - neither the stand's page load nor …" (:3193-3195, fires on every keyed profile with e2e rows, i.e. every such
story) AND j1's "the stand's full page load is 12 s (measured …)". FR-10 (one packet does not contradict itself). If a
release is cut between the merges, users get it. Fix 17.

Order — I checked the three sibling r2 cards the designer did not read (file-name grep over each):
- `20261117-rules-debt-wave3-k-cards-r2.md` §0.1-0.2 (:23-43) says the opposite of card §E: "C3-j is HELD … Without C3-j:
  C3-j leaves both queues … If C3-j lands later, it is the later merger: it merges main in, re-derives its own row's pins".
  Its queues are `gate-registry.json`/`test_gate_registry.py`: C3-g → C3-k1 → C3-k2 → C3-k3 → C3-k4 → C3-h, and
  `gate_preflight.py`: C3-k2 → C3-h. The card's `C3-rr → C3-j1 → C3-j2 → C3-k2 → C3-h` contradicts it.
- k3 (k r2 :578, :583, :638, :650) OWNS `scripts/manual_capture.py` (import line :99-100, `stand_probe` :1612-1613) and
  `scripts/tests/test_manual_capture.py` — both in j1's owns. A new conflict the card's §E asked to be ordered.
- `judgment-census.json` is written by g-h r2, k r2 (k4 :722) and conversions r2 — and, after Fix 11, by j1 as well as j2.
- `gate-registry.json`/`test_gate_registry.py`: all three r2 files; j2 measures its pins as deltas (S-f), which is sound.
Fix 15.

## K6. Architecture and principles — PARTLY FAILS

- AR-22, AR-10, AR-13, AR-28, AR-12, AR-20: kept as designed (subject to K1/K4 completeness).
- AR-14 / AR-15 / P31 (one action, one road) — FAILS. The package already has ONE road for a fact about a stand that the
  factory learns: the answer registry `records/project-knowledge.json`, one writer `project_knowledge.record`, catalogue rows
  `store: registry, scope: stand` in `config-keys.json` `knowledge` — and it is used for a MACHINE-found fact, not only a
  person's: `environments.sign_in` (`config-keys.json:712`: "The way in a first look found … Writer:
  first_look.record_sign_in through project_knowledge.record"; `first_look.py:1003-1011`), `environments.stand_lessons`
  (:711, read by `brief_pack.stand_lesson_lines`, which the card itself takes as its model). The card opens a third store
  (`stand-page-load.json`) with its own reader/writer, its own key, no lock, and no way out (AR-25: a wrong row has no revoke
  door; `project_knowledge.py revoke` exists for registry rows). Even the record-family helpers it cites as precedent are
  not reused: `environment_record.load_rows`/`write_rows` (:208-243, docstring "ONE reader of a record file") — the card
  prescribes `event_store.atomic_json` and its own unreadable handling instead. Fix 2.
- AR-3 not named in §1 although j1 stores a project fact outside the config (and AR-3's carrier list names the registry).
  Fix 2 names it.
- AR-4 — FAILS for `failed` rows (K3). Fix 3.
- AR-29 / P27 — code measures data, holds. But §1's "reviewed by `qa-code-critic` (a tier above judges the role)" has no
  carrier: no charter line, no `judgments.d/code.json` row; the only carrier is the brief line. Fix 12.
- AR-29 census — FAILS: "j1 adds no census unit" is wrong. `test_judgment_census.py` u1: a function named `check_*` IS a unit
  and demands a row (`test_judgment_census.py:15-17`); precedent `check_stand_lessons` (notes only, never raises) has row
  `judgment-census.json:422` shape/data. j1 does not own `judgment-census.json`. Fix 11.
- P1, P5, P27: kept (the factory's own browser is the route; the role keeps the judgment of the waits).
- P2 (universality): "frontend address" is NOT a project assumption by itself — `frontend_of` is the one reader and returns
  `""` when there is none — but treating its absence as a failure/defect IS one (API-only, device stands). Fix 4.
- FR-56 / AR-11 (only the context a role needs): `STAND_LOAD_ROLES` adds S6 `qa-runner` with no reason; the closest
  precedent, `test_timeout_line`, goes to S5 and S7 only (`brief_pack.py:4560`). Fix 10.

## K7. Tests against docs/TESTING.md — PARTLY FAILS

- Rows in existing tables, expectations from the card: right form.
- The DoD carries no `test: <file::table> | expected from: <source>` line per behaviour item (TESTING.md «Строка теста в DoD»
  :75-89; `tools/dispatch_manifest.py` checks its presence above the designer threshold). Fix 18.
- A 10 000-row record file is an internal boundary (the file is written by the factory's one writer), and with Fix 2 the file
  reader is already tested where it lives; 0-byte/broken/list rows likewise. «внутренняя граница без своей двери» / no
  mini-battery on an internal function (:55-56). Fix 18.
- Outside input (the address from the project's config, the stand name) keeps its battery: address AT 120 / 121, userinfo,
  non-ASCII name — right.
- New module `stand_load.py` (or, after Fix 2, the new reader) is covered by no keep row: `scenario_walk.witness_for`
  (:888-926) maps a script to keep rows by `covers`; `test-layers.json` `test_manual_capture.py.covers` (:3017-3030) does not
  list it, so the DoD's `--witness-for` prints "run the whole scenario layer" for it. j1 does not own `test-layers.json`.
  Fix 19.
- j1's trigger rows: the gate-A test files that run `gate_preflight.run(…, "A")` on a config with a stand + e2e-ui or
  manual-agent row and no `MC.BACKEND_FACTORY` stub would now launch a REAL browser (30 files call the gate in tests; the
  `story()` fixture of test_gate_preflight.py has no environments, so `test_the_rehearsal_writes_nothing` :1578 stays green —
  checked :98-132). Unenumerated. Fix 20.
- Volume: no estimate is asked of the designer; the builder's `tests-over:` line applies. n/a at plan level.

## K8. Written for a weaker model — PARTLY FAILS

Good: files, functions, expected texts, the direction chosen, expected-from per item. Defects a weaker builder would trip on
(each verified on b89871b3):
- `stand_identity.definition_sha_for(cfg, environment_id: str)` takes the stand NAME (`stand_identity.py:149`); the card passes
  the stand dict. Fix 9.
- "the builder STOPS if the backend has no navigation call" — it has one (`goto`), with `StepTimeout` vs `StepFailed`. Fix 9.
- "an address that reader refuses (credentials in it)" — the reader refuses nothing of the kind (K3). Fix 6.
- `timeout_for` signature change with callers outside owns (K1) → the builder must stop mid-node. Fix 1.
- `_stand_pick` returns a tuple `(entry, name, said)`; say which element (`[1]`, as `brief_pack.py:4545`). Fix 9.
- The trigger "an automate row of level E2E_LEVEL keyed to a profile not handed" — point at the code that does exactly this
  today (`_e2e_limit` :3110-3114 + `check_s5_stand_limits` :3183-3189) so the builder lifts it rather than reinvents it.
  Fix 9.

## K9. F-home — the proposed P32 and the FR-50 sentence are NOT faithful

The owner's full first word (r1 :896-898): «Почему не гоняем? Почему лимиты не измерены? Вообще любой стенд который нам
дали мы считаем готовым тестовым стендом если человек не скажет чего-то дополнительного (например мы видим что доступа
куда-то нет, спрашиваем как его получить и человек говорит: на этом стенде этого доступа в принципе нет). И то можем
предложить моки.» The card's §0 cuts it at «дополнительного…».
- LOST: (a) the example — when access is missing the factory DOES ask, and asks HOW TO GET it; only a person's "this stand
  has no such access" overrides readiness. P32's «человека не спрашивают о числе, которого он не знает» is right for numbers
  but, without the access half, reads as "never ask about the stand"; (b) the mocks — even then, the factory may offer mocks.
  Neither text has it. (c) «измерить и использовать» — P32 keeps "measures" and drops "uses"; the owner tied measuring to a use
  ("для того чтобы тесты правильно написать?").
- ADDED: FR-50 "nor waited on for" is not in the words (harmless, but it is an addition); "a number they cannot know"
  generalises «этот лимит … точно не знает» — acceptable as a principle, say so to the owner.
- Proposed P32 (to show the owner): «Любой стенд, который нам дали, — готовый тестовый стенд, пока человек не скажет иного.
  Чего не хватает (например, доступа), фабрика спрашивает — как это получить; если человек говорит, что на этом стенде этого
  нет вовсе, фабрика принимает это и может предложить моки. Число о стенде, которое нужно работе (например, время загрузки
  страницы для ожиданий в тестах), фабрика измеряет сама и использует; человека о нём не спрашивают — он его не знает.
  Понятие, которое никому не нужно, удаляется.»
- Proposed FR-50 sentence: "A stand the factory is given is a ready test stand unless a person says otherwise. What the work
  is missing on it (an access) is asked as how to get it; when the person says the stand does not have it at all, that is
  accepted and mocks may be offered. A number about the stand that the work uses is measured by the factory and used; a
  person is never asked for it."
Fix 22.

---

## Standing questions (plan gate)

- DUPLICATION AND CONSISTENCY (brief item 6): FAILS — a second store for stand facts beside the registry and a reader/writer
  that copies `environment_record.load_rows/write_rows` (Fix 2); `measurement_is_stale` duplicated for a merge window by
  design (E13) where a delegation is free (Fix 8); two contradicting notes in the window (Fix 17); the two "Lead decisions"
  blocks at the end restate the same forks with different provenance (keep one; Fix 16).
- CODE QUALITY (brief item 7): n/a at plan level beyond the above; the never-raise discipline, the `extra` machine fields and
  no field path in a sentence (FR-6) are right.
- ONE ACTION, ONE ROAD (brief item 12, P31): FAILS — the separate record file (Fix 2). The n/a branch for a stand with no web
  page (Fix 4) serves the task's own condition and reaches no shared mechanism differently — not an exclusion.
- TESTS (question 5): see K7 — Fixes 18-20.

## Class completeness (rule 5, by SIBLING_MAP)

- Axis 5 (stage twins): brief lines one formatter — covered by the card; the role set fixed by Fix 10.
- Axis 16 (one JSON reader): covered by Fix 2 (registry / `ER.load_rows`, not a new reader).
- Axis 18 (ratchet raise in the diff that adds the site): the census row j1 adds (Fix 11) — named raise if a ceiling moves.
- Axis 32 (where judgment lives: census ↔ gates ↔ charters): Fixes 11, 12.
- Axis 34 (one road): Fix 2.
- Axis 4 (rules ↔ debt ↔ principles): debt line → S1b (legit); P32/FR-50 → owner (Fix 22).
- Same class outside the node: the reporter `timed_out` card (Fix 21).

## Fixes (each executable; the designer/Lead applies them in the round)

1. **j1 owns, callers.** Add to j1 `owns`: `scripts/investigation_probe.py` (:419) and `scripts/walk_session.py` (:1221).
   Replace the known-callers list in item 3 with the full list on b89871b3: `gate_preflight.py:2808`; `manual_capture.py:3015,
   3178, 3413, 5383`; `investigation_probe.py:419`; `walk_session.py:1221`. Each has `cfg` and the project root in scope
   (`MC.load_config` returns both) — say so; the builder still greps and reports per hit.
2. **One store (P31, AR-14, AR-3, AR-25).** Store the measurement through the answer registry, like `environments.sign_in`:
   a new `config-keys.json` `knowledge` row `environments.page_load` (`store: registry`, `scope: stand`, `compare: exact`,
   `absent_means: "not measured on this stand yet: the default limit applies"`, `needed_by` the readers, a `note` naming
   writer `stand_load.record → project_knowledge.record` and reader), written only through `project_knowledge.record`,
   read through one `project_knowledge` reader (or a thin `stand_load.read` over it), revocable by `project_knowledge.py
   revoke`. Key it by stand name plus `definition_sha` as the card does (E8). Drop `RECORD_REL`/`stand-page-load.json`, the
   own atomic write and the own unreadable handling (the registry's reader gives them, with the lock at
   `project_knowledge.py:46`). Name AR-3 in §1 ("a measured stand fact lives in the answer registry, one writer"). Owns:
   `references/config-keys.json`, `scripts/project_knowledge.py` (only if a reader function is added). If the Lead prefers
   to keep the file, the card must instead (a) build on `environment_record.load_rows`/`write_rows` with a
   `schema_version`, (b) give a way out (a revoke CLI or "delete the row" door named in the note text), (c) name AR-3, AR-14,
   AR-25 and P31 with the reason the registry does not fit — not leave them silent.
3. **`failed` is never recorded (AR-4, FR-41).** Only `measured` rows (incl. `at_least`) are written. A `failed` measurement
   is told in the gate note and retried at the next gate A. Add a max age for reuse: a `measured` row older than
   `REUSE_DAYS = 7` (constant in `stand_load`) is measured again, besides the `verified` rule — `verified` is written once at
   onboarding, so without an age a rebuilt stand keeps its old number forever. Rewrite E3/E8 and §C's "A `failed` row is
   reused" accordingly; test rows: a failed measurement → nothing recorded, the next rehearsal measures again; a row 8 days
   old → measured again; 6 days → reused.
4. **No web page → `n/a`, not `failed` (P2, FR-19).** Trigger only when a browser surface is used: an e2e-ui automate row
   (as today), or a manual case whose surface is the UI (read the surface the way `check_actor_sign_in` decides it needs a UI
   sign-in — name the function). A stand whose `frontend_of(...)["url"]` is `""` or that carries `surface` (a device stand)
   → state `n/a`: nothing measured or recorded, no gate note, the brief line `- Stand page load: not applicable (the stand has
   no web address).` E2 rewritten; test row: an http-only manual case on a stand without a frontend → no browser, no note.
5. **Reason words by owner (FR-19, FR-3).** `failed.why` carries a cause class, and the note/brief name the owner by it:
   `no_browser` ("this machine has no browser the factory can start"), `unreachable` (`StepFailed` on goto: "the stand did not
   answer at {address}"), `outside_hosts` (the navigation was blocked by the stand-host guard: "the address leads outside the
   stand's hosts"), `factory` (any other exception: "a defect of the factory"). Only `factory` says "a defect of the factory".
   One test row per class.
6. **Userinfo in the address.** `stand_load.measure` refuses an address whose `urlsplit(...).username or .password` is set:
   state `failed`, cause `credentials_in_address`, why "the stand's web address carries a user name or password; it is not
   opened or stored". The `address` field is never written with userinfo. Delete "an address that reader refuses" from
   item 1 and E16 (the reader refuses nothing of the kind, `env_probe.py:421-427`).
7. **Duplicate stand names.** Two `environments[]` rows with the selected name → no measurement, no record, gate note "two
   stands are named {name}; the page load is not measured until one name is unique" (no question); brief `none`. One test row.
8. **One staleness body from j1 on (AR-15).** In j1, `gate_preflight.measurement_is_stale` becomes `return
   stand_load.is_stale(at, verified)` (the body moves, the gate keeps a one-line delegate); j2 deletes the delegate. E13's
   "exists twice for one merge window" is removed (the clone ratchet would otherwise see the copy).
9. **Concrete anchors for the builder.** In item 1: the navigation is `backend.goto(address)`, which returns the elapsed
   seconds (`manual_capture.py:1814-1815`, `_timed` :1801-1812); `MC.StepTimeout` → `at_least`; `MC.StepFailed` → `failed`
   (cause per Fix 5); delete the STOP clause. `definition_sha_for(cfg, stand_name)` takes the name. `_stand_pick(...)[1]` is
   the name. The trigger is lifted from `_e2e_limit` :3110-3114 and `check_s5_stand_limits` :3183-3189 (keyed, non-handed
   profiles whose cases have an `e2e-ui` automate row). State that an `at_least` row gives `timeout_for` = 180 + 30 = 210.
10. **Roles.** `STAND_LOAD_ROLES = {("S5","qa-automator"), ("S5","qa-code-critic"), ("S7","qa-failure-analyst")}` — the
    `test_timeout_line` set; S6 `qa-runner` only with a named use (it writes no waits and judges none). Adjust item 4, the
    changelog (S5/S7) and the test rows.
11. **Census row in j1 (AR-29, AR-20).** j1 owns `scripts/tests/fixtures/judgment-census.json` and adds
    `{"file": "gate_preflight.py", "function": "check_stand_page_load", "class": "shape", "roles": ["conductor"], "owner":
    "data"}` (precedent `check_stand_lessons`, :422). Replace "j1 adds no census unit" (§1 table, §2 architecture content).
    If `test_judgment_census.py` (canon) shows a ceiling move (`blocking_per_role`), it is a named raise in j1's commit,
    recovered by j2's deletion of :418. Add j1 to the census queue in §E.
12. **Where the waits' fit is judged — say the carrier.** Either (a) state that the brief line ("Page-object waits are written
    to fit it") in the S5 automator AND code-critic heads is the only carrier, and drop "reviewed by `qa-code-critic` (a tier
    above judges the role, AR-29)" from §1, or (b) add a code-critic judgment row/charter line in owns (with the role-load
    ratchet named). Recommend (a): no new role text.
13. **Catalogue.** j1 adds its new readers to `config-keys.json` `needed_by` (`environments`: the measurement and the brief
    reader; plus the new `knowledge` row of Fix 2); j2 removes `gate_preflight.py:check_s5_stand_limits` (:724) and
    `gate_preflight.py:_stand_limit_card` (:733). Both nodes own `references/config-keys.json` (row-disjoint edits).
14. **j2 test deletions, whole.** Add to j2 owns' text: every runner-list line in `test_gate_preflight.py`'s main block that
    calls a deleted test (by NAME, not by the five words — e.g. :6244, :6246, :6248, :6264 and the lines of every test in
    :2734-2935); the helpers `record_edit` (:4072-4077), `with_limits` and the `record` lambda of `scenario_messages`
    (:3758-3760) with all their callers. The report gives one line per deleted name.
15. **§E order = the k-cards r2.** Rewrite §E: j1 and j2 are LATER mergers after the k-series on every shared file
    (`gate_preflight.py`: after C3-k2 and C3-h; `gate-registry.json`/`test_gate_registry.py`: after C3-k4 and C3-h;
    `manual_capture.py`/`test_manual_capture.py`: after C3-k3; `judgment-census.json`: after k4, g, conversions), each merging
    main in and re-deriving its pins as deltas (S-f) — as `wave3-k-cards-r2.md` §0.1 (:31-33) already says. Or, if the Lead
    wants j first, edit the k r2 §0.2 queues in the same move; the two files may not disagree.
16. **One carrier of the direction.** Update batch row RD1-13 (`batch-1-phase-2.md:41`) — direction (C), two nodes j1/j2, the
    new zones (j1: stand_load.py, gate_preflight.py, manual_capture.py, brief_pack.py, investigation_probe.py, walk_session.py,
    config-keys.json, judgment-census.json, test-layers.json, scaffold.py, the three test files; j2 as listed + config-keys.json)
    — under TEAMWORK §2 (taken batch); mark the finding `20261117-rd2-c3-j-…otvet-v-reestre.md` "superseded by card r2 (owner,
    17.11.2026)". Keep ONE "Lead decisions" block in the card (the second one, which leaves F-home to the owner), delete the
    other.
17. **No contradicting notes in the window (FR-10).** j1 and j2 merge to main in ONE wave with no release cut between them —
    write it as an invariant in §E and in F-j-split; or j1 suppresses `check_s5_stand_limits`'s `unmeasured` note when the
    new step recorded a measurement (one line in j1, deleted with the check in j2). Recommend the wave invariant.
18. **Test lines and trimming (TESTING.md).** Add a `test: <file::table> | expected from: <§>` line per behaviour item to j1's
    and j2's DoD. Drop the 10 000-row and the 0-byte/broken/list rows for the record (internal file; after Fix 2 its reader is
    tested where it lives) — keep ONE "unreadable registry → brief says it could not be read" row. Keep the outside-input
    rows (address AT 120 / 121, userinfo, non-ASCII stand name).
19. **test-layers.json.** j1 owns `scripts/tests/test-layers.json` and adds the new module (if Fix 2 keeps `stand_load.py`) to
    the `covers` of the keep row whose table tests it (`test_manual_capture.py`, :3017), so `--witness-for` names it.
20. **Fixture and real-browser risk.** j1 owns `scripts/tests/fixtures/manual-evidence/scaffold.py`: remove `measured` from
    the `localhost` stand (:68) and give the scaffold a helper that records a 70 s measurement through the one writer, called
    where the tests relied on 70 + 30 (`test_manual_capture.py:194, 262, 273, 951, 1040, 1558, 1660`), so those expectations
    keep their 100 s and now prove the round trip (AR-22). Before dispatch the Lead greps the 30 test files that run gate A
    (`gate_preflight.run(`/`Rehearsal(` under `scripts/tests/`) for a config with `environments` plus an `e2e-ui` or
    `manual-agent` row and no `BACKEND_FACTORY` stub; each hit joins j1's owns with a stub of `stand_load.measure`
    (a module seam, default the real one), or the card names why it does not trigger.
21. **Sibling: the reporter timeout question.** `gate_preflight.py:3635-3641` asks the person to "raise
    `gate_rehearsal.reporter_timeout_s`" — the same class as the owner's word (a number the person does not know). Proposed
    node for the Lead (rules-debt pile, after j2): the reporter's one-test timeout is `max(reporter_timeout_s, measured load +
    margin)` and a timeout is reported (note, the profile's report "unproven"), not asked. It waits for the owner's word on
    F-home (P32) — a line in «Остатки»: `reporter timed_out card asks a person for a timeout | узел: <new id, rules-debt>`.
22. **F-home texts.** Replace the P32 and FR-50 proposals in §D with the two texts in K9 (access → ask how to get it; "no such
    access here" → accepted, mocks may be offered; a needed number → measured and used, never asked; an unneeded concept →
    deleted). Quote the owner's first word whole in §0 (r1 :896-898), not cut at «дополнительного…».

---

## Trail

Read: the card r2 whole (:1-460); r1 :885-901; `wave3-k-cards-r2.md` :1-60, grep of shared file names and :570-590, :638,
:650, :722; `wave3-g-h-cards-r2.md` :28-45 and file-name grep; `c3-fix-conversions-cards-r2.md` file-name grep;
`gate_preflight.py` :150-210, :2780-2825, :3085-3340, :3630-3649, :5139-5146, :6060-6110; `manual_capture.py` :100-115,
:229, :550-575, :1658-1694, :1798-1817, :3005-3018, :3170-3180, :5375-5386, `_first_line`; `investigation_probe.py` :405-425;
`walk_session.py` :1205-1225; `env_probe.py` :405-480; `stand_identity.py` :129-161; `environment_record.py` :1-60,
:200-250; `project_knowledge.py` grep (:1-12, :43-46, :110-115); `first_look.py` :1003-1011; `brief_pack.py` :2734-2745,
:2881-2895, :4136-4150, :4530-4565, :3395-3410; `config-keys.json` :120-135, :706-741 (grep); `architecture.md` :62-77
(AR-3, AR-4); `judgment-census.json` :4, :418, :422; `test_judgment_census.py` :1-40; `test_gate_preflight.py` :30-140,
:1578-1595, :3648-3656, :3712-3760, :3804-3811, :4068-4080, :6244-6249; `test_manual_capture.py` :160-197, :1036-1044 and a
grep of the 100-s expectations; `fixtures/manual-evidence/scaffold.py` :55-75; `test-layers.json` :3010-3030;
`scenario_walk.py` :888-932; `test_config_migration.py` :370-410; `factory-rules-debt.md:111`; the finding file; batch row
RD1-13 (`batch-1-phase-2.md:41`, :51); `docs/TESTING.md` :36-95, :131-185; `docs/SIBLING_MAP.md` axis headings;
`critic_verdict.schema.json`; `critic-diff-brief.md` :1-40.
Searches with positive controls are named inside K1 and K4.
Run: `python -B scripts/tests/scenario_walk.py --witness-for <abs>/stand_load.py` (and `.../manual_capture.py`) under
`timeout 60` — printed nothing (killed by the timeout while importing `selftest`; not used as evidence). The `witness_for`
behaviour for an uncovered script was established by reading `scenario_walk.py:888-926` instead.
Not done (scout-scale, for the Lead): zone overlap of the new j1 owns (`brief_pack.py`, `manual_capture.py`,
`walk_session.py`, `investigation_probe.py`, `config-keys.json`) against every batch "в работе" — 40 batch files mention one
of these names; `python tools/piles.py check` is the door.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "j1 changes timeout_for's signature but does not own its callers investigation_probe.py:419 and walk_session.py:1221 (also unnamed manual_capture.py:3015, 3178)",
    "fixture scaffold.py:68 writes measured.e2e_page_load_s=70 and test_manual_capture.py:194/262/273/951/1040/1558/1660 depend on 70+30; not in owns, not in the card",
    "check_stand_page_load is a census unit by name (test_judgment_census u1); the card claims none and j1 does not own judgment-census.json",
    "failed rows are recorded in a carried record and reused until definition sha or verified changes: one outage or one browserless machine disables measurement for every machine (AR-4, FR-41)",
    "a third store for stand facts beside the answer registry, own reader/writer, no lock, no way out (P31, AR-14, AR-25; precedent environments.sign_in via project_knowledge.record)",
    "API-only and device stands become failed and 'a defect of the factory' (P2, FR-19)",
    "frontend_of does not refuse credentials; a userinfo address would be stored and printed",
    "section E order contradicts wave3-k-cards-r2 section 0.1-0.2; k3 owns manual_capture.py and test_manual_capture.py",
    "j1/j2 window shows two contradicting notes in one gate A packet (FR-10)",
    "P32/FR-50 texts drop the owner's access-and-mocks half and the 'use' of 'measure and use'"
  ],
  "fixes": [
    "1 add investigation_probe.py and walk_session.py to j1 owns; list all timeout_for callers",
    "2 store the measurement through project_knowledge.record under a new knowledge row environments.page_load, or justify a separate file with ER.load_rows/write_rows, a way out and named AR-3/14/25/P31",
    "3 never record failed rows; retry next gate A; measured rows reused at most REUSE_DAYS=7 besides the verified rule",
    "4 no web address or device stand -> n/a, no browser, no note; trigger only on a UI surface",
    "5 failed.why carries a cause class; only the factory class says defect of the factory",
    "6 refuse and never store an address with userinfo; remove the claim that frontend_of refuses it",
    "7 duplicate stand names -> no measurement, a note, brief none",
    "8 j1 makes gate measurement_is_stale a one-line delegate to stand_load.is_stale",
    "9 name goto/StepTimeout/StepFailed, definition_sha_for(cfg, name), _stand_pick()[1], the lifted trigger, at_least -> 210",
    "10 STAND_LOAD_ROLES = S5 automator, S5 code critic, S7 failure analyst unless a use for S6 is named",
    "11 j1 owns judgment-census.json and adds the check_stand_page_load shape/data row; a ceiling move is a named raise",
    "12 name the brief line as the only carrier of the waits judgment and drop 'reviewed by qa-code-critic', or add a charter row in owns",
    "13 config-keys.json needed_by: j1 adds its readers, j2 removes check_s5_stand_limits and _stand_limit_card",
    "14 j2 deletes every runner line calling a deleted test by name and the helpers record_edit, with_limits, the record lambda",
    "15 rewrite section E as later merger after the k-series per k r2 section 0.1, or edit k r2 in the same move",
    "16 update batch row RD1-13 and mark the r1 finding superseded; keep one Lead decisions block",
    "17 j1 and j2 merge in one wave with no release between (invariant), or j1 silences the old unmeasured note",
    "18 add test:/expected from: lines per item; drop the 10000-row and record-file corruption rows",
    "19 j1 owns test-layers.json and adds the new module to the covers of its test file",
    "20 j1 owns scaffold.py: record 70 s through the one writer; Lead greps the 30 gate-A test files for unstubbed triggers before dispatch",
    "21 propose a rules-debt node for the reporter timed_out card that asks a person to raise reporter_timeout_s",
    "22 replace the P32 and FR-50 texts with the K9 versions and quote the owner's first word whole"
  ],
  "class_completeness": "Axes 5, 16, 18, 32, 34, 4 walked (see Class completeness). Same-class sibling outside the node: the reporter timed_out card gate_preflight.py:3635-3641 (fix 21). Zone overlap of the new j1 owns across batches in work is scout-scale and returned to the Lead (piles.py check).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md",
      "docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md:885-901",
      "docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md:1-60,570-590,638,650,722",
      "docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md:28-45",
      "docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards-r2.md (file-name grep)",
      "ai-packages/qa-factory/scripts/gate_preflight.py:150-210,2780-2825,3085-3340,3630-3649,5139-5146,6060-6110",
      "ai-packages/qa-factory/scripts/manual_capture.py:100-115,550-575,1658-1694,1798-1817,3005-3018,3170-3180,5375-5386",
      "ai-packages/qa-factory/scripts/investigation_probe.py:405-425",
      "ai-packages/qa-factory/scripts/walk_session.py:1205-1225",
      "ai-packages/qa-factory/scripts/env_probe.py:405-480",
      "ai-packages/qa-factory/scripts/stand_identity.py:129-161",
      "ai-packages/qa-factory/scripts/environment_record.py:1-60,200-250",
      "ai-packages/qa-factory/scripts/first_look.py:1003-1011",
      "ai-packages/qa-factory/scripts/brief_pack.py:2734-2745,2881-2895,3395-3410,4136-4150,4530-4565",
      "ai-packages/qa-factory/references/config-keys.json:120-135,706-741",
      "ai-packages/qa-factory/design/architecture.md:62-77",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json:4,418,422",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:1-40",
      "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py:30-140,1578-1595,3648-3811,4068-4080,6244-6249",
      "ai-packages/qa-factory/scripts/tests/test_manual_capture.py:160-197,1036-1044",
      "ai-packages/qa-factory/scripts/tests/fixtures/manual-evidence/scaffold.py:55-75",
      "ai-packages/qa-factory/scripts/tests/test-layers.json:3010-3030",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py:888-932",
      "plans/piles/rules-debt/batch-1-phase-2.md:41,51",
      "plans/piles/rules-debt/findings/20261117-rd2-c3-j-s5-stand-limits-otvet-v-reestre.md",
      "docs/TESTING.md:36-95,131-185",
      "docs/SIBLING_MAP.md (axis headings)"
    ],
    "reruns": [
      {
        "command": "grep -rliE 'page_object_max_wait_s|e2e_page_load_s|_e2e_limit|stand_limit|check_s5_stand_limits|measurement_is_stale|limit_seconds|skip_stand_limits' ai-packages/qa-factory",
        "result": "hits: factory-rules-debt.md, config-keys.json, gate-registry.json, cost_capture.py (unrelated _limit_seconds), gate_preflight.py, manual_capture.py, judgment-census.json, scaffold.py, five test files; no brief_pack.py, no onboarding text"
      },
      {
        "command": "grep -rn 'timeout_for' ai-packages/qa-factory/scripts --include=*.py (outside tests)",
        "result": "gate_preflight.py:2808, investigation_probe.py:419, manual_capture.py:555 (def), 3015, 3178, 3413, 5383, walk_session.py:1221"
      },
      {
        "command": "python -B scripts/tests/scenario_walk.py --witness-for <abs>/stand_load.py (timeout 60)",
        "result": "no output (killed by the 60 s timeout during import); not used as evidence, scenario_walk.py:888-926 read instead"
      }
    ]
  }
}
```
