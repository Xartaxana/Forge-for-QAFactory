# Card C3-j r3: the stand's page load, measured by the factory and used; the wait and the code comparison deleted (t-1132, node rules-debt/1/RD1-13, F19)

Designer fix round for the Lead. It REPLACES card r2 (`docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md`) whole and r1 §2
(`docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md`). A builder executes a node from THIS file alone. Inputs: the two plan
verdicts on r2 — V1 `docs/tasks/specs/reviews/t-1123-c3-j-card-r2-plan.md` (READY WITH FIXES, Fixes 1-22) and V2
`docs/tasks/specs/reviews/t-1123-c3-j-r2-plan.md` (GO WITH FIXES, F1-F11) — and the Lead decisions that stand (end of this file).

**Base.** The root checkout (`main`; HEAD `9d45c8d9` per the session's git status; I did not read `.git` refs). Every `file:line` below
was re-read in this round unless the trail says otherwise. No shell: nothing was RUN; every command is for the builder or the Lead.

## §0. The direction: the owner's two words of 17.11.2026, whole

1. «Почему не гоняем? Почему лимиты не измерены? Вообще любой стенд который нам дали мы считаем готовым тестовым стендом если человек
   не скажет чего-то дополнительного (например мы видим что доступа куда-то нет, спрашиваем как его получить и человек говорит: на
   этом стенде этого доступа в принципе нет). И то можем предложить моки.»
2. «зачем нам вообще знать этот лимит? Для того что бы тесты правильно написать? Ну значит надо измерить и использовать. Человек точно
   этот лимит не знает. А если нам он не нужен, то вообще это понятие удалить».

What binds every text of this card:
- NO branch asks a person for the number, and no branch puts a factory-, machine- or stand-owned reason to a person as a choice (FR-3).
- The half of the limit that has a user (the stand's page load) is measured by the factory AND used (j1). The half that has none (the
  page objects' wait and the code comparison) is deleted whole (j2). This is F-j0 = (C), decided.
- The measured number is a FLOOR, never a ceiling (V2 F2/K7): it may only LENGTHEN a limit and every text says "pages behind the
  sign-in can be slower". A signed-out landing time that SHORTENED a limit would cut a sign-in short and ask a person after all.

## §A. Evidence: who produces and who reads the two halves (corrected)

| half | producer today | readers today (all on the root checkout) |
|---|---|---|
| page load, config `environments[].measured.e2e_page_load_s` | none in shipped code. Only a TEST fixture writes it: `scripts/tests/fixtures/manual-evidence/scaffold.py:68` (value 70) | `gate_preflight._e2e_limit` :3089-3164 (feeds `check_s5_stand_limits` :3166-3218, `check_s5_reporter`'s `over` skip :3323-3330), `_stand_limit_card` :3243-3273 (other stands, :3250-3252), and `manual_capture.timeout_for` :555-562, called at `gate_preflight.py:2808`, `manual_capture.py:3015, 3178, 3413, 5383`, `investigation_probe.py:419`, `walk_session.py:1221` (Grep `timeout_for\(` over `scripts/`; positive control: the definition :555) |
| page objects' wait, config `profiles[].page_object_max_wait_s` | none | only `_e2e_limit` :3119 |

Positive-controlled searches (this round): Grep, case-insensitive, `e2e_page_load_s|page_object_max_wait_s|skip_stand_limits` over
`ai-packages/qa-factory/` → `gate_preflight.py` 9, `manual_capture.py` 1, `scaffold.py` 1, `test_gate_preflight.py` 11,
`test_manual_capture.py` 8 (the gate hits are the control). `references/config-keys.json` names the deleted FUNCTIONS in `needed_by`
(:724 `profiles` → `gate_preflight.py:check_s5_stand_limits`; :733 `environments` → `gate_preflight.py:_stand_limit_card`).
The roles that will read the measurement (automator, code critic, failure analyst) are PROPOSED readers, wired by j1.

What follows: an AR-22 defect today (fields read, nothing produces them; M5, t-1092, 3/3 recorded stories); the load half has users,
the wait half has none.

## §1. Architecture, rules, owners (designer rule 1)

FR sections walked. j1: A (FR-3, FR-19: each failure names its true owner; FR-59), B (FR-6, FR-10: notes in plain words; one packet
does not contradict itself — §E wave invariant), C (FR-38/AR-10: the number reaches the automator before the work; FR-15), D (FR-59:
no gate decides on it), E (FR-53/P8: a no-trace story writes nothing into the project), F (FR-41: "at least" and "not measured" are
never written as facts; FR-28), G (FR-47, FR-30, FR-32). j2: A, B (texts removed), C (FR-13/AR-1 untouched), D, G.

AR-n touched, with the change check each demands IN THE DoD:

| AR | how kept | change check (in the DoD) |
|---|---|---|
| AR-3 | the measured stand fact lives in the project's answer registry (`records/project-knowledge.json`), catalogued by a `knowledge` row with an `absent_means` | the catalogue row exists; `test_project_knowledge.py` FIVE_KEYS pin names it |
| AR-14 | ONE writer of the registry: `project_knowledge.record` (called by `check_stand_page_load` only for this key) | Grep `PAGE_LOAD_KEY` over `scripts/` outside tests: writers only `gate_preflight.py:check_stand_page_load` via `PK.record` |
| AR-13 | ONE reader of the measurement: `project_knowledge.page_load`; `timeout_for` and `brief_pack` call it; the address is read through `env_probe.frontend_of`, the stand card through `project_knowledge.environment` | the same Grep: readers only through `PK.page_load` |
| AR-22 | the first producer lands WITH its readers in j1 (record → `page_load` → `timeout_for`, the brief line, the gate note); j2 deletes the wait key with every reader | round-trip rows (a recorded measurement read by `timeout_for` and by the brief); Grep `page_object_max_wait_s|e2e_page_load_s` over `scripts/` outside tests = 0 after j2 |
| AR-25 | a wrong measurement has a way out: `project_knowledge.py revoke --id PK-n` (existing door), plus age and definition rules | a revoked row reads `none` (test row) |
| AR-4 | the row is keyed by stand name + `definition_sha` + measured address; a MACHINE fact ("no browser here") is never recorded | rows: other sha → none, other address → none; a failed measurement records nothing |
| AR-10 | the S5 automator and code-critic heads and the S7 failure-analyst head carry the measured load | `test_brief_pack.py` rows |
| AR-11 | only those three (stage, role) pairs; not the S5 plan dispatch; no line when nothing is measured | rows: S3 strategist none, S5 plan none, `none` state no line |
| AR-12 | one headless load per stand per 7 days (or per definition/address change), only when an e2e-ui or manual row will use it | gate rows: reuse = no second call; no use = no call |
| AR-15 | one staleness body: `gate_preflight.measurement_is_stale`'s body moves to `project_knowledge.stale_against_verified`; j1 leaves the gate a one-line delegate, j2 deletes it | Grep `def measurement_is_stale` = 0 after j2 |
| AR-20 | j1 adds census row `check_stand_page_load` (a named raise if a ceiling moves); j2 deletes `check_s5_stand_limits` (shrink), registry row and pins by the named delta | `test_judgment_census.py` (canon) and `test_gate_registry.py` (canon), named |
| AR-28 | `none` / `unreadable` / failed causes are named in every reader; nothing gates on them, so none is ever a pass at a boundary | rows per state |
| AR-29 | code measures a number (data); whether waits fit it is the automator's judgment; no code comparison is left (j2) | census rows below |

Checks added, moved or removed (AR-29; P27):

| check | node | owner it serves | census class | blocks |
|---|---|---|---|---|
| `gate_preflight.check_stand_page_load` (gate A: measure or reuse; a note either way) | j1 | data (code) | NEW row `shape`, roles `["conductor"]`, owner `data` (precedent `check_stand_lessons`, `judgment-census.json:422`) | no (notes only) |
| `project_knowledge.record_problems` gains the page-load shape branch `_page_load_value_faults` | j1 | data | unit unchanged: `record_problems` shape (`judgment-census.json:856`); the helper carries the comment "part of the record_problems unit" (precedent :635, :654) | as today (refuses a write) |
| `manual_capture.measure_page_load`, `project_knowledge.page_load`, `brief_pack.stand_page_load_lines` | j1 | data | no unit (names outside `UNIT_NAME_RE`, `test_judgment_census.py:17-19`; never raise) | no |
| whether the page objects' waits fit the load | j1 (moved from code to role) | judgment: `qa-automator`; its only carrier is the brief line in the S5 automator and code-critic heads (V1 Fix 12 (a): no charter line is added, and the card claims no "tier above" review beyond the code critic reading the same line) | none (role) | n/a |
| `check_s5_stand_limits` + `_e2e_limit` + `_stand_limit_card` + the reporter's `over` skip | j2 (deleted) | intent: the owner's word (a person is not asked; an unneeded concept is deleted) | row `gate_preflight.py::check_s5_stand_limits` shape/data (`judgment-census.json:418`) leaves: a shrink, named | was yes |

Commit lines: in the form `tools/architecture_gate.py` accepts (the only carrier of the grammar; not copied here). Each node gives the
CONTENT. `judgment: none` always carries its ` -- <why>`.

## §2. Node C3-j1: the factory measures the stand's page load and hands it to whoever writes or judges waits

Queue: §E (after C3-h; j1 and j2 merge in ONE wave). Plan critic: this round is the r2 critics' fix round; a re-review only if the Lead
judges F-j-store (a) an architecture change (PROJECT.md new-idea step 6).

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`, this file §0-§G; under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/project_knowledge.py:1-260,440-525,586-812`, `scripts/manual_capture.py:95-120,140-240,482-562,1640-1700,1801-1816,2688-2700,2990-3031,3170-3180,3405-3416,5375-5386`, `scripts/gate_preflight.py:150-210,1531-1541,1665-1670,2338-2360,2689-2811,3077-3241,5139-5146,6078-6110`, `scripts/brief_pack.py:2734-2746,2881-2894,3361,3389-3407,4133-4153,4515-4560`, `scripts/env_probe.py:449-470`, `scripts/stand_identity.py:129-154`, `scripts/investigation_probe.py:410-425`, `scripts/walk_session.py:1215-1225`, `scripts/first_look.py:1002-1045` (the registry-write precedent), `references/config-keys.json:705-741`, `references/manual-evidence.md:50-60`, `scripts/tests/fixtures/judgment-census.json:1-5,418-422,856`, `scripts/tests/fixtures/manual-evidence/scaffold.py:60-82`, `scripts/tests/test_project_knowledge.py:975-1050`, `scripts/tests/test_manual_capture.py:160-200,255-275,945-955,1036-1044,1460-1470,1550-1560,1655-1680`, `scripts/tests/test_gate_preflight.py:30-62,2143-2262,3651,3800-3811,6018-6046`, `scripts/tests/test_brief_pack.py:2402-2442` (and grep `stand_lesson_lines`)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/project_knowledge.py` (`PAGE_LOAD_KEY`, `PAGE_LOAD_ELEMENT`, `PAGE_LOAD_REUSE_DAYS`, `HOW_PAGE_LOAD`; `SOURCES` + `"measured"`; `BY` + `"gate"`; `_page_load_value_faults` and its branch in `record_problems`; new reader `page_load`; new `stale_against_verified`; the module docstring's usage lines)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py` (new `measure_page_load`; new seam `PAGE_LOAD = None` beside `BACKEND_FACTORY` :229; `timeout_for` new signature and body; its callers :3015, :3178, :3413, :5383; NOT the import line :99-100, which C3-k3 owns: j1 uses lazy imports inside its functions)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (new `check_stand_page_load`, `_page_load_due`; its place in `run`'s gate A tuple; `run`'s docstring; `measurement_is_stale` becomes a one-line delegate; the `timeout_for` call :2808) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/investigation_probe.py` (the call :419 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/walk_session.py` (the call :1221 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py` (new `stand_page_load_lines`, constant `STAND_LOAD_ROLES`, one call in the head build after :4544)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json` (`knowledge` row `environments.page_load`; `needed_by` additions of `environments` :733 and `gate_rehearsal` :741)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/manual-evidence.md` (line :57 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (one new row only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/manual-evidence/scaffold.py` (delete the `measured` block :68 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py` (FIVE_KEYS pin :987-999; rows of item 1)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py` (`timeout_for` rows :171-181; the 100-s expectations moved to 180 s; rows of item 2)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (default stub at import beside `_install_the_tripwire` :62; rows of item 3; `check_stand_page_load` added to `NEW_CHECK_FUNCTIONS` :3651 and to the FR-6 scan list :3809)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py` (rows of item 4; `ROLE_BRIEF_BYTES_MAX` :2411 only on a measured, named raise — expected none)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-c3-j1-stand-page-load.md` (new)
non-goals: anything of the old limit (`_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`, `limit_seconds`, the reporter skip: j2); the module docstring line `gate_preflight.py:57` (j2); `references/gate-registry.json` (the measurement judges nothing: §C); `report_facts.py` (no report line: §C); `manual_capture.element_wait_for`; the reporter's `timed_out` card (fork F-j-reporter); a signed-in measurement (route (b), later node); `scripts/tests/test-layers.json` (no new module: §C); `scripts/tests/test_brief_pack_s5_plan.py` (the plan dispatch gets no line); asking a person anything; any new test file
handoff: report path given by the Lead
edges: E1-E20 (§B)
DoD: (1) `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/project_knowledge.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/investigation_probe.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/walk_session.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json C:/QAFactory/forge-repo/ai-packages/qa-factory/references/manual-evidence.md C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/manual-evidence/scaffold.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py` and the printed non-slow files; (2) the Grep tool, case-insensitive, pattern `PAGE_LOAD_KEY|environments\.page_load` over `ai-packages/qa-factory/scripts/` excluding `tests/`: writers only in `gate_preflight.py:check_stand_page_load` (through `PK.record`), readers only through `PK.page_load` (AR-13/14), positive control: the same call finds `project_knowledge.py`; (3) the brief ratchet: the report quotes the `RATCHET ROLE_BRIEF_BYTES_MAX` lines of `qa-automator`, `qa-code-critic`, `qa-failure-analyst` and `RATCHET S5_PLAN_BRIEF_BYTES_MAX` before and after (expected equal: the seed records no measurement, E15); slow files (`test_gate_preflight.py`, `test_judgment_census.py`, `test_brief_pack.py` if listed slow) are named and judged by the batch canon.
  test: test_project_knowledge.py::FIVE_KEYS pin + record_problems rows + page_load rows | expected from: §2 item 1, E6-E10, E17, AR-3/13/14/25
  test: test_manual_capture.py::measure_page_load table + timeout_for table | expected from: §2 item 2, E3-E5, E11-E13, V2 F2
  test: test_gate_preflight.py::check_stand_page_load rows | expected from: §2 item 3, E1, E2, E14, E16-E19, owner 17.11.2026
  test: test_brief_pack.py::stand_page_load_lines rows | expected from: §2 item 4, E15, E20, AR-10/11
  test: none -- prose and catalogue (manual-evidence.md :57, config-keys rows, changelog) | expected from: §2 items 5-6 (DOC-DISPATCH witness: the keys `environments.page_load`, `180 s, or the measured page load + 30 s when that is longer` quoted verbatim, script source attached, with a negative control)
siblings: axis 5 (prose twins): the builder greps `skills/qa-story/phases/s4.md`, `s5.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `agents/qa-failure-analyst.md`, `references/manual-evidence.md` for `page load|timeout|wait` and gives each hit "checked, no edit" or an edit inside owns (outside owns: a question); axis 34 (one road): the measurement sits at gate A, which both roads pass (`driver_gates.py:120`, `skills/qa-story/phases/s4.md:19`, V2 K "ONE ROAD: PASS"); the reporter `timed_out` card is the same class outside this node (fork F-j-reporter)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md` (C3-j1)

Items (each names file, function, behaviour, test):

1. **`project_knowledge.py`: the registry carries the measurement (F-j-store (a)).**
   - Constants beside `SIGN_IN_KEY` (:66): `PAGE_LOAD_KEY = "environments.page_load"`; `PAGE_LOAD_ELEMENT = "frontend"` (one subject per
     stand: what was measured is the stand's frontend start page); `PAGE_LOAD_REUSE_DAYS = 7`; `HOW_PAGE_LOAD = "measured by the factory's
     headless browser at gate A, signed out, one full load of the start page"`.
   - `SOURCES` (:129) gains `"measured"`; `BY` (:130) gains `"gate"`. The refusal sentences :753, :755 list them automatically.
   - `_page_load_value_faults(element, value) -> list`, commented `# part of the record_problems unit (shape of a measured page load); not
     a unit of its own`. Faults (each a sentence ending "; nothing was recorded"): element is not `PAGE_LOAD_ELEMENT`; `value` not a dict
     with EXACTLY the keys `load_s, at_least, address, definition_sha, at`; `load_s` not a finite number > 0 (a bool is not a number);
     `at_least` not a bool; `address` not an `http(s)://` string or carrying a user name or password (`urlsplit(...).username or
     .password`); `definition_sha` not a non-empty string; `at` not a string that `ER._moment` parses. Form only (AR-29).
   - `record_problems` (:701): a branch `elif key == PAGE_LOAD_KEY: out += _page_load_value_faults(element, value)` placed BEFORE the role
     rules, beside the lessons/sign-in branches (:734-740). INVARIANT (positional): a page-load row never meets the role rules, and a role
     key never skips them.
   - `stale_against_verified(at, verified) -> str`: the body of `gate_preflight.measurement_is_stale` (:195-204), moved verbatim (one body,
     AR-15).
   - `page_load(root, cfg, stand) -> dict`, PURE, never raises. Returns `{"state", "load_s", "at_least", "address", "at", "why"}` with
     `state` one of `measured`, `none`, `unreadable`. In this order:
     1. `stand` empty or `PLACEHOLDER_STAND` → `none` (why `no stand`);
     2. `PAGE_LOAD_KEY not in KEYS` → `unreadable` (why `CATALOGUE_PROBLEM` or "the catalogue has no row for environments.page_load");
     3. `load(root)` problem → `unreadable` (why the problem);
     4. `_latest(rows, PAGE_LOAD_KEY, stand, PAGE_LOAD_ELEMENT)` None (absent file, no row, revoked row) → `none`;
     5. `_page_load_value_faults` non-empty → `none` (why `malformed`): the safe side is the default limit;
     6. `environment(stand, root, cfg)` not found (incl. "two stands are named") → `none` (why its problem);
     7. `value["definition_sha"] != stand_identity.definition_sha_for(cfg, stand)` → `none` (why `another stand definition`);
     8. `value["address"] != manual_capture._safe_url(env_probe.frontend_of(cfg, stand, root=root)["url"])` → `none` (why `another
        address`) (V2 F5);
     9. `value["at"]` older than `PAGE_LOAD_REUSE_DAYS` days before now (`ER._moment`, `ER.now_iso`) → `none` (why `older than 7 days`)
        (V1 Fix 3);
     10. `stale_against_verified(value["at"], entry.get("verified"))` non-empty → `none` (why it);
     11. else `measured` with the value's fields.
     Lazy imports inside the function (`stand_identity`, `env_probe`, `manual_capture`) so no import cycle.
   - Module docstring: one paragraph naming the key, its one writer (`gate_preflight.check_stand_page_load` through `record`), its one
     reader (`page_load`) and its exit (`revoke`).
   - expected from: AR-3/13/14/25 (V1 Fix 2), FR-59 direction "toward the default", P8 (`_refuse_no_trace` :586 applies as for every row).

2. **`manual_capture.py`: the measurement and the limit.**
   - Seam `PAGE_LOAD = None  # (cfg, stand_name, project_root) -> measurement dict; tests replace it` beside `BACKEND_FACTORY` (:229).
   - `measure_page_load(cfg, stand_name, project_root) -> dict`, never raises. In this order:
     1. `entry = project_knowledge.environment(stand_name, root=project_root, cfg=cfg)`; not found → `{"state": "failed", "cause":
        "factory", "why": <its problem>}` (the gate filters duplicates before calling, so this is a defect);
     2. the entry names `surface` (a device stand, `stand_identity.py:133-135`) → `{"state": "n/a", "why": "a device stand has no web
        page"}`;
     3. `url = env_probe.frontend_of(cfg, stand_name, root=project_root)["url"]`; `""` → `{"state": "n/a", "why": "the stand has no web
        address"}` (V1 Fix 4, P2);
     4. `urlsplit(url).username or .password` → `{"state": "failed", "cause": "credentials_in_address", "why": "the stand's web address
        carries a user name or password"}`; the address is not opened and not returned (V1 Fix 6; `frontend_of`/`frontend_address`
        :421-427 accept such an address, so this check is ours);
     5. `hosts = set(stand_hosts(cfg, root=project_root))`; backend = `BACKEND_FACTORY()` when set, else `PlaywrightBackend()`;
        `BrowserUnavailable` or any exception of the constructor or of `open(...)` → `{"state": "failed", "cause": "no_browser", "why":
        _first_line(exc)}`; `open(DEFAULT_TIMEOUT_S, hosts, None, element_wait_for(cfg))`;
     6. `mark = backend.event_mark()` when the backend has it; `seconds = backend.goto(url)` (:1814-1815: `wait_until="load"`, the limit
        is `open`'s timeout, returns elapsed seconds through `_timed` :1801-1812);
        - returned → `{"state": "measured", "load_s": max(0.1, round(seconds, 1)), "at_least": False, ...}`;
        - `StepTimeout` (caught BEFORE the generic handler) → `"load_s": float(DEFAULT_TIMEOUT_S), "at_least": True`;
        - `StepFailed` → if `backend.events_since(mark)` holds a `blocked` event (the route guard :1674-1683 aborted a host outside the
          stand) → cause `outside_hosts`, else cause `unreachable`; `why` = `_first_line(exc)`;
        - any other exception → cause `factory`, why `<type>: <first line>`;
     7. `backend.close()` in `finally` (an exception of `close` is swallowed);
     8. a `measured` result also carries `"address": _safe_url(url)`, `"definition_sha": stand_identity.definition_sha_for(cfg,
        stand_name)` and `"at": _now()`.
   - `timeout_for(project_root, cfg, stand) -> float` (was `timeout_for(env)`): `name = str((stand or {}).get("name") or "")`; when
     `project_root` and `name` are given, `got = project_knowledge.page_load(project_root, cfg, name)`; `measured` → `max(DEFAULT_TIMEOUT_S,
     got["load_s"] + TIMEOUT_MARGIN_S)`; every other state, or any exception → `DEFAULT_TIMEOUT_S`. It no longer reads `stand["measured"]`.
     Values: recorded 70 → 180; 160 → 190; `at_least` (180) → 210 (V2 F2, V1 Fix 9). The docstring and the constant comments :108-109
     say "the measurement may only lengthen it".
   - Every caller changes in this commit: `gate_preflight.py:2808` (`self.project_root, self.config, stand`), `manual_capture.py:3015,
     3178, 3413, 5383`, `investigation_probe.py:419` (`cfg, project = MC.load_config(task)` is at :416), `walk_session.py:1221`
     (`self.project_root`, `self.cfg`). A caller with no project root in scope passes `None` (→ 180, the safe side) and the report names
     it. The builder greps `timeout_for\(` over `scripts/` and gives one report line per hit (known: 8 call sites).
   - expected from: V2 F1/F2, V1 Fixes 1, 4, 5, 6, 9; FR-19 (cause = owner); AR-13.

3. **`gate_preflight.py`: `check_stand_page_load` at gate A.**
   - Position: in `run`'s gate A tuple (:6086-6094) right after `r.check_s5_stand_limits` and before `r.check_stand_lessons`.
     INVARIANT (positional): no step before it reads the measurement except through `timeout_for`, which errs to 180 s; `check_actor_sign_in`
     (earlier) gets 180 s in a project's first rehearsal, the safe side; after j2 no step reads the old limit.
   - `_page_load_due(self) -> bool`: True when (a) a keyed profile not in `self._handed()` has a case whose automate row level is
     `E2E_LEVEL` — lifted from `_e2e_limit` :3110-3114 and `check_s5_stand_limits` :3183-3189, not reinvented — or (b)
     `plan_rows_of(self.task_root, ("manual-agent",))` is non-empty (every manual capture takes its page limit from `timeout_for`).
   - Body, in this order (no `add`, ever: it blocks nothing and asks nothing — owner, 17.11.2026; FR-3):
     1. `self.project_root is None`, `self._gate_switch("skip_stand_limits")` or not `_page_load_due()` → return, no note;
     2. `name = str(self._selected_environment().get("name") or "")`; empty → return;
     3. `card = PK.environment(name, cfg=self.config)`; not found and its problem names two stands → note "two stands are named {name}; the
        page load is not measured until one name is unique" (V1 Fix 7), return; any other problem → note "the stand {name} could not be read
        ({problem}); the page load is not measured this time", return;
     4. `got = PK.page_load(self.project_root, self.config, name)`; `measured` → reuse note, return (no browser);
        `unreadable` → note "what the factory keeps about this project could not be read ({why}), so the page load is not measured this
        time", return (nothing could keep it);
     5. `result = (MC.PAGE_LOAD or MC.measure_page_load)(self.config, name, self.project_root)`;
     6. `n/a` → return, no note (E2); `failed` → one note by cause (texts below), nothing recorded (F-j-failed (a));
     7. `measured` → `PK.record(self.project_root, key=PK.PAGE_LOAD_KEY, environment=name, element=PK.PAGE_LOAD_ELEMENT, state=PK.KNOWN,
        scope="stand", value={load_s, at_least, address, definition_sha, at}, words=PK.HOW_PAGE_LOAD, source="measured",
        story=self.task_root.name, by="gate", where="gate A", task_root=self.task_root)`; a `TimeoutError` (busy lock) is the problem "the
        record was busy"; then one note: the measured text, plus " It was not kept for the next stories ({problem})." when the row was
        refused (a no-trace story: `PK.NO_TRACE_WORDS`).
   - Every note carries machine `extra` fields (`state`, `cause`, `load_s`, `at_least`, `address`, `why`) and no field path, script, flag or
     exit code in the sentence (FR-6; the t-357 rule test reads every note).
   - Note texts (address = `_safe_url`, cut at 120 characters with `…`):
     - measured now: "The stand's start page ({address}) loaded in {load_s:g} s, measured now by the factory's browser while signed out;
       pages behind the sign-in can be slower. The S5 and S7 briefs carry it, and manual checks wait at least 180 s, longer when this load
       needs it."
     - measured, at least: "... had not finished loading after 180 s (so it takes at least that long) ..."
     - reused: same text with "measured on {at[:10]}" instead of "measured now".
     - failed, by owner (FR-19): `no_browser` "The factory could not measure the stand's page load: this machine has no browser the factory
       can start. Manual checks wait 180 s per page; it is measured again at the next rehearsal."; `unreachable` "... the stand did not
       answer at {address} ..."; `outside_hosts` "... the start page leads to a host outside the stand's hosts ..."; `credentials_in_address`
       "... the stand's web address carries a user name or password, so it is not opened or kept ..."; `factory` "... a defect of the factory
       ({why}) ...". Only `factory` says "a defect of the factory". Each ends "Manual checks wait 180 s per page; it is measured again at
       the next rehearsal."
   - `measurement_is_stale` (:195) becomes `return project_knowledge.stale_against_verified(at, verified)` (lazy import) — j2 deletes it
     (V1 Fix 8).
   - `run`'s docstring (:6079-6080): it now names a second write — the page-load row through `project_knowledge.record`, project level,
     refused in a no-trace story.
   - expected from: owner 17.11.2026; P31 (gate A is the one point both roads pass); FR-3, FR-19, FR-59; V1 Fixes 3, 5, 7, 8.

4. **`brief_pack.py`: `stand_page_load_lines(project, cfg, env_name) -> list`.**
   - `STAND_LOAD_ROLES = {("S5", "qa-automator"), ("S5", "qa-code-critic"), ("S7", "qa-failure-analyst")}` beside `FIRST_LOOK_KIND`
     (:4141) (V1 Fix 10: `qa-runner` writes and judges no waits).
   - Call, after :4544 in the head build, as its own statement: `if (stage, role) in STAND_LOAD_ROLES and s5_kind != "plan": head +=
     stand_page_load_lines(project, hooklib.load_config() or {}, str(pipeline.get("environment") or ""))` (V2 F3 (ii): the plan
     dispatch writes no waits). For S7, `s5_kind` is not "plan" by construction; the builder confirms the variable is defined at that point
     for every stage, else uses the guard `stage == "S7" or s5_kind != "plan"`.
   - The stand is `_stand_pick(cfg, env_name)`: its `[0]` None → `[]`; its name `[1]` goes to `PK.page_load(project, cfg, name)`.
   - Lines (one at most):
     - measured: `- Stand page load: the start page {address} loaded in {load_s:g} s ({at[:10]}, the factory's browser, signed out); pages behind the sign-in or heavier routes can be slower. Fit your waits to the slowest load your own runs show, never below this.`
     - at least: `- Stand page load: the start page {address} did not finish loading within 180 s ({at[:10]}, the factory's browser, signed out), so it takes at least that long. Fit your waits to the slowest load your own runs show, never below 180 s.`
     - unreadable: `- Stand page load: could not be read ({why}).`
     - `none`, no stand, an ambiguous stand: `[]` — NO line (V2 F3 (i); the brief claims nothing, AR-23: the empty outcome is "no line",
       declared in the docstring).
     - an exception: `- Stand page load: not read ({type}), a defect of the factory` (precedent `test_timeout_line` :3405-3407).
   - The address is cut at 120 characters with `…` (AT 120 whole, 121 cut). It reports; it judges nothing (P1, AR-7).
   - expected from: AR-10, AR-11, FR-38, FR-41; V2 F2 (floor wording), F3.

5. **Catalogue and prose.**
   - `config-keys.json` `knowledge`: `"environments.page_load": {"store": "registry", "compare": "exact", "scope": "stand", "absent_means":
     "not measured on this stand yet: every page limit is 180 s and the briefs carry no number", "needed_by": ["project_knowledge.py:page_load",
     "manual_capture.py:timeout_for", "brief_pack.py:stand_page_load_lines", "gate_preflight.py:check_stand_page_load"], "note": "The stand's
     start-page load the factory measured at gate A, signed out; one row per stand (element frontend). Writer: gate_preflight.check_stand_page_load
     through project_knowledge.record (source measured, by gate), never in a no-trace story. Reader: project_knowledge.page_load (definition,
     address, 7 days and the stand's verified date decide whether it still speaks). A wrong row has one exit: project_knowledge.py revoke.",
     "ask_when": null}` — after the `environments.sign_in` row (:712).
   - `needed_by` additions (V1 Fix 13, V2 F6): `environments` (:733) + `manual_capture.py:measure_page_load`, `project_knowledge.py:page_load`;
     `gate_rehearsal` (:741) + `gate_preflight.py:check_stand_page_load` (the off switch, E14).
   - `references/manual-evidence.md:57`: "the stand's measured page load + 30 s (else 180 s)" → "180 s, or the measured page load + 30 s when
     that is longer" (V2 F2; FR-37).
   - `judgment-census.json`: `{"file": "gate_preflight.py", "function": "check_stand_page_load", "class": "shape", "roles": ["conductor"],
     "owner": "data"}` beside :422 (V1 Fix 11). If `test_judgment_census.py` (canon) shows a ceiling move (`blocking_per_role`), it is a named
     raise in j1's commit, recovered by j2's deletion of :418.
   - `scaffold.py:68`: delete the `measured` block (V1 Fix 20, V2 F4).

6. **Tests: rows in existing keep tables** (expectations from this card, never from the code's output).
   - `test_project_knowledge.py` (keep, register): FIVE_KEYS gains `"environments.page_load"` after `"environments.sign_in"` (:987-999, its
     comment names t-1132); `record_problems` rows: a valid value accepted with source `measured`, by `gate`; element `ui` refused; `load_s`
     0 / -1 / True / NaN / `"12"` refused; an extra key refused; an address with `user:pw@` refused; a missing `at` refused. `page_load` rows:
     absent file → none; a recorded row → measured (round trip); another `definition_sha` → none; another address → none; `at` 8 days old →
     none, 6 days → measured; `at` older than the stand's `verified` → none; a revoked row → none; an unreadable registry → unreadable; a
     non-ASCII stand name round-trips; a no-trace story's `record` is refused with `NO_TRACE_WORDS` (P8).
   - `test_manual_capture.py` (keep, detector): table `measure_page_load`, fake backend through `BACKEND_FACTORY`: goto 12.34 s → 12.3,
     `at_least` False; `StepTimeout` → 180.0, `at_least` True; goto 179.9 → 179.9, `at_least` False (AT the cap); `StepFailed` with a
     `blocked` event → `outside_hosts`; `StepFailed` without → `unreachable`; constructor raises `BrowserUnavailable` → `no_browser`; a
     `RuntimeError` in goto → `factory`, `close` still called; no frontend → `n/a`; a `surface` stand → `n/a`; `http://u:p@host` →
     `credentials_in_address`, backend never constructed, no `address` key. `timeout_for` table (replaces :171-181): config `measured` 70 is
     no longer read → 180; recorded 70 → 180; recorded 160 → 190; recorded at least 180 → 210; `none` / `unreadable` → 180; `project_root`
     None → 180. The scaffold-based expectations that leaned on 70 + 30 move to 180 s: :194 ("the default limit 180 s"), :262 ("the limit
     is 180 s"), :269-273 (wait 180000 ms AT), :951 (AT 180 / BEYOND 180.001), :1040 (comment), :1467 `LANDING_LIMIT = MC.DEFAULT_TIMEOUT_S`
     with its comment, :1558 ("within 180 s"), :1660 (label "poll 720, 180 s"). The builder greps the file for `100` near `limit` and gives
     one line per hit (V2 F4: the count is "not established" at plan time).
   - `test_gate_preflight.py` (keep, gate_named): at import, beside `_install_the_tripwire()` (:62), a default `MC.PAGE_LOAD` stub that
     returns `{"state": "failed", "cause": "no_browser", "why": "no browser in this test"}`, so no test of the file launches a real browser
     (V1 Fix 20); rows replace it with a recording fake: an e2e row and no record → one note, no finding, a registry row written, fake called
     once; a second rehearsal → reuse note, no call; a failed measurement → note with its owner words, no finding, `can_proceed` unchanged,
     nothing recorded, the next rehearsal calls again; no e2e row and no manual row → no call, no note; `skip_stand_limits` → no call, no
     note; only a handed profile, no manual row → nothing; two stands named `localhost` → the duplicate note, no call; a stand with no
     frontend → `n/a`, no note; a no-trace story (`pipeline.no_trace`) → measured, the note says it was not kept, no registry file;
     a recorded measurement of 160 → the sign-in probe opens with 190 (the `_ProbeBrowser` world of :6018-6046 records `open`'s timeout).
     `check_stand_page_load` joins `NEW_CHECK_FUNCTIONS` (:3651) and the FR-6 scan list (:3809).
   - `test_brief_pack.py` (keep, detector): measured line for the S5 automator, the S5 code critic and the S7 failure analyst; the at-least
     line; the unreadable line; no line for S3 `qa-test-strategist`, for the S5 plan dispatch, for `none`; an address of 200 characters cut
     at 120 with `…` (AT 120 whole, 121 cut). The ratchet rows stay as they are (E15).
   - Not written (TESTING.md: internal boundary): a 10 000-row registry, 0-byte/broken/list files (the registry's reader is tested where it
     lives; ONE unreadable row is kept above) (V1 Fix 18).
   - Real-browser risk in the other 44 test files that run gate A (Grep `gate_preflight\.run\(|GP\.run\(|Rehearsal\(|"--gate"` over
     `scripts/tests`: 45 files, 220 hits): CI installs no Playwright (Grep `playwright`, case-insensitive, over `.github/`: 0 hits; positive
     control `pip install|python` over the same folder: 100 hits), so there the step adds one `no_browser` note and records nothing. Info
     pinned wholesale: Grep `\["info"\]\s*==|r\.info ==|\["info"\], \[\]` → 2 hits, `test_gate_role_accounts.py:300` (runs only
     `check_role_accounts`) and `test_probe_debt.py:425` (not a gate run): neither reaches the step. A developer machine with Playwright
     pays one launch against a dead `localhost:5173` per full gate run (estimate, not measured). The canon names any other pin; a red pin is
     a `defect_found` against j1 (rule 4).

7. **Changelog fragment** (English, FR-30): the gate measures the stand's start-page load once per stand definition (headless, signed out),
   keeps it in the project's answer registry, the S5 automator/code-critic and S7 failure-analyst briefs carry it, and the manual capture's
   page limit becomes "180 s, or the measured load + 30 s when longer"; `gate_rehearsal.skip_stand_limits: true` now means "do not measure
   the page load" (V2 F10).

architecture content: `AR-3 -- the measured stand fact lives in the answer registry under a catalogued knowledge row`; `AR-14 -- one writer, project_knowledge.record, called by check_stand_page_load`; `AR-13 -- one reader project_knowledge.page_load; timeout_for and the brief call it`; `AR-22 -- the first producer of the page load lands with its readers`; `AR-25 -- a wrong row leaves by project_knowledge.py revoke`; `AR-4 -- keyed by stand, definition sha and address; a machine fact is never recorded`; `AR-10 -- the automator's brief carries the load before the work`; `AR-28 -- none/unreadable/failed causes named in every reader, nothing gates on them`; `AR-29 -- check_stand_page_load is a shape/data census row; the fit of waits is the automator's judgment`. judgment content: `none -- code measures a number and reports it; no check moves into or out of a role; the waits stay the automator's`.

## §3. Node C3-j2: the wait and the code comparison deleted whole

Serial after j1 on j1's branch (same HOT file; its tests read j1's world); merges in the SAME wave as j1 (§E).

given: as j1, plus the j1 diff; `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json:479-499`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py:36-75,200-210,245-255,320-350,735-750,1000-1060`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json:410-420`; `C:/QAFactory/forge-repo/tools/architecture_gate.py` (its census rule, `CENSUS_REL` :88); `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py:2730-2936,3060-3090,3515-3530,3620-3660,3700-3770,3800-3811,4068-4136,6200-6290`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (delete `_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`, `limit_seconds` :157-164, the delegate `measurement_is_stale`, their selftest lines (:6394, :6398 on r2's base: the builder greps), `r.check_s5_stand_limits` in `run` :6089, `check_s5_reporter`'s `over` skip :3323-3330 and its `profiles`/`entry` use if then unused, the docstring mentions :57, :804, and the `E2E_LEVEL` comment :152-153 if the constant keeps a reader (`_page_load_due`): reword, else keep) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (delete row `s5_stand_limits` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json` (remove `gate_preflight.py:check_s5_stand_limits` from `profiles` :724 and `gate_preflight.py:_stand_limit_card` from `environments` :733 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (delete row `gate_preflight.py::check_s5_stand_limits` :418 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (deletions listed in item 4)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (`EXPECTED_IDS` :45, `EXPECTED_DEBT` :63, K-T1.2 :252, K-T1.14 :328, :342-343, D13 if it moves; one AR-20 comment line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-c3-j2-stand-limit-removed.md` (new)
non-goals: `test_story_run_delivery_b.py:555`, `test_story_run_delivery_c.py:975, :987` (they use the id `e2e_stand_limit` as sample data of a generic finding; no code of theirs reads the check: one report line each); `design/factory-rules-debt.md` (its line moves by S1b, RD1-23); `environment_record.py`, `gate_brief.py`, `stand_gaps.py` (r1's road is dropped); the j1 functions; any new test file
handoff: report path given by the Lead
edges: E21-E24 (§B)
DoD: (1) `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, `s5_stand_limits` absent from its output, the debt count one lower than on j2's base; (2) the Grep tool, case-insensitive, over `ai-packages/qa-factory/scripts/` excluding `tests/`, pattern `page_object_max_wait_s|e2e_page_load_s|_e2e_limit|check_s5_stand_limits|_stand_limit_card|measurement_is_stale|limit_seconds` → 0, positive control: the same call finds `stand_page_load_lines` in `scripts/`; the same pattern over `references/config-keys.json` → 0 (positive control: `check_stand_page_load` found there); (3) `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; `test_gate_preflight.py`, `test_gate_registry.py`, `test_judgment_census.py` are slow: canon, named; (4) the report gives one line per deleted test function and per deleted runner line, by NAME.
  test: test_gate_registry.py::EXPECTED_IDS/EXPECTED_DEBT/K-T1.2/K-T1.14/D13 | expected from: §3 item 3 (delta from the base, S-f)
  test: test_judgment_census.py (canon, the row's absence) | expected from: §3 item 2, AR-20
  test: test_gate_preflight.py::test_the_reporter_proves_a_profile_with_one_of_its_own_tests (existing, unchanged: the reporter now rehearses every non-handed profile) | expected from: §3 item 1, E22
siblings: axis 5 (row ↔ sites ↔ prose): the builder greps the package `.md` files for `stand limit|page_object|e2e stand` and gives each hit a line; the A1 class ("a word compared in an unregistered function"): the reporter's `== "over"` leaves with the skip
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md` (C3-j2)

Items:
1. **`gate_preflight.py` deletions**, as listed in owns. After them `check_s5_reporter` rehearses every keyed, non-handed profile; on a
   slow stand its own timeout (`reporter_timeout_s`, default 180, :3312) and its outcome states say what happened (E22). `run`'s tuple
   loses `r.check_s5_stand_limits`; `r.check_stand_page_load` stays where j1 put it. `gate_rehearsal.skip_stand_limits` keeps its one
   reader, `check_stand_page_load` (E23).
2. **Registry and census**: row `s5_stand_limits` deleted (no gate is left to decide on the unknown, FR-59); census row :418 deleted, the
   shrink named in the verdict (AR-20). The builder reads `tools/architecture_gate.py` for what the `judgment:` line must say about a census
   change; if it demands what this card does not give, the node stops and returns a question.
3. **`test_gate_registry.py` pins**, measured at build as deltas from j2's base (S-f): `EXPECTED_IDS`/`EXPECTED_DEBT` lose
   `s5_stand_limits`; K-T1.2 reads `"<N-1> gate(s) left as debt:"` (N = the base's count, measured); K-T1.14: the debt list follows
   `EXPECTED_DEBT`, its "six rows" wording moves, the split goes debt -1, total -1, converted unchanged; a comment line `C3-j2, t-<id>:
   s5_stand_limits deleted (owner, 17.11.2026)`; F4 :743-747 unchanged (the row was `target`); D13 re-measured with `GR.analyse(PLUGIN_ROOT)`
   before and after — expected: no triple leaves; a different set is a stop and a question.
4. **`test_gate_preflight.py` deletions, whole (V1 Fix 14)**, each with its runner-list line in the file's main block, found by NAME (not
   by the five words):
   - helpers `with_limits` :2736, `limit_cards` :2748, `record_edit` :4072;
   - tests `test_k5_a_page_that_loads_slower_than_the_page_objects_wait_is_one_card` :2752, `test_k5_strict_greater_than_at_and_beyond_the_wait`
     :2792, `test_k5_nothing_recorded_is_not_measured_and_never_a_card` :2801, `test_k5_a_limit_that_cannot_be_read_is_one_defect_and_no_card`
     :2832, `test_a_measurement_older_than_the_stand_is_not_a_measurement` :2861, `test_the_other_stand_is_named_only_when_its_own_load_fits`
     :2879, `test_a_card_a_person_has_answered_is_closed_in_all_the_ways_it_can_still_be` :2894, `test_the_stand_limit_step_can_be_switched_off`
     :2924, `test_the_reporter_skips_a_profile_whose_e2e_limit_card_is_open` :3065 (whole: its "fits" half :3078 proved the skip's other
     side), `test_c2_the_stand_limit_card_offers_only_doors_that_have_an_executor` :3624, `test_q2_a_page_load_with_no_command_or_date_is_the_factorys_defect`
     :4080 (runner :6271);
   - edits: `test_the_cmp2_rehearsal_is_the_one_a_person_can_read` :3518 loses its `with_limits` config and the "stand limit is a question
     of the gate" check :3520-3523 (the rest stays); `scenario_messages` :3740 loses the `record` lambda :3758-3759 and the three `limits` runs
     :3760-3764; `NEW_CHECK_FUNCTIONS` :3651 and the list at :3809 lose `_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`; the
     `_e2e_limit` entry at :3715 goes;
   - the builder then greps the file for `e2e_stand_limit|s5_stand_limits|_e2e_limit|page_object_max_wait_s|e2e_page_load_s|with_limits|record_edit|limit_cards`
     → 0, and runs the file's import (`python -B -c "import ast,sys;ast.parse(open(sys.argv[1],encoding='utf-8').read())" <file>`) plus a
     Grep of every runner-list call name against the file's `def` names (no NameError left).
5. **Changelog fragment**: the gate no longer compares a recorded page-object wait with the stand; `environments[].measured.e2e_page_load_s`
   and `profiles[].page_object_max_wait_s` are no longer read (a config that carries them is unaffected).

architecture content: `AR-22 -- the wait key, read with no producer, is deleted with every reader and catalogue entry`; `AR-7 -- no code compares a test's waits with the stand; the automator does, with the measured number`; `AR-15 -- the staleness delegate goes; one body remains in project_knowledge`; `AR-20 -- registry row and census unit removed, pins moved by the named delta, D13 re-measured`; `AR-28 -- no gate is left on this unknown`. judgment content: `none -- a check is deleted on the owner's word; nothing moves into judgment and no person is asked`.

## §B. Edges (each with the INVARIANT it protects)

- **E1 (no stand / a placeholder stand / no project root)**: nothing measured, recorded or noted; `timeout_for` 180; no brief line.
  INVARIANT: nothing is recorded under an empty or placeholder stand (`record_problems` refuses it too).
- **E2 (an API-only stand, a device stand)**: `n/a`: no browser, no note, no row, no brief line. INVARIANT: a stand without a web page is
  never called a failure or "a defect of the factory" (P2, FR-19).
- **E3 (no browser on this machine)**: cause `no_browser`, a note naming the machine, nothing recorded, retried at the next gate A.
  INVARIANT: a machine fact never enters a carried record (AR-4); a factory/machine reason is reported, never asked (FR-3).
- **E4 (limit: beyond the cap)**: `StepTimeout` → `load_s` 180, `at_least` True; texts say "at least"; `timeout_for` 210. INVARIANT: an
  unfinished load is never written as its true value (FR-41).
- **E5 (limit: AT the cap)**: a load finishing at 179.9 s is `measured` 179.9 (`timeout_for` 209.9); only the backend's timeout makes
  `at_least`. INVARIANT: the cap is the backend's limit, one number (`DEFAULT_TIMEOUT_S`).
- **E6 (signed out)**: the start page is measured without an account (often a login page); every text says "signed out" and "pages behind
  the sign-in can be slower". INVARIANT: the number is a FLOOR; no text claims a signed-in or deep route was measured, and no limit is
  ever SHORTER than 180 s because of it (V2 F2).
- **E7 (the stand down / refusing)**: cause `unreachable`, the stand named as the owner; nothing recorded; retried next gate A.
  INVARIANT: a moment of downtime never disables the measurement (V1 Fix 3, V2 F7).
- **E8 (a redirect outside the stand's hosts)**: the route guard aborts it; cause `outside_hosts` (the config's: the stand's hosts do not
  cover the start page's redirect). INVARIANT: a capture never leaves the stand, and the owner named is the config, not the factory.
- **E9 (reuse and staleness)**: reused while the row's `definition_sha` and address equal today's, it is ≤ 7 days old and not older than the
  stand's `verified`; otherwise measured again. INVARIANT: a measurement of another stand definition, address or build never speaks for
  this one (AR-4).
- **E10 (registry unreadable / catalogue without the row)**: `page_load` → `unreadable`; the gate does not measure and says so; the brief
  says it could not be read; `timeout_for` 180. INVARIANT: a file the factory cannot read is never written over (`record` refuses), and an
  unknown is never a number (FR-59).
- **E11 (credentials in the address)**: `credentials_in_address`; never opened, never stored, never printed. INVARIANT: no user name or
  password reaches a record or a brief.
- **E12 (outside input: the address)**: a 200-character address is cut at 120 in notes and briefs (rows AT 120 / BEYOND 121); a
  non-ASCII stand name round-trips. INVARIANT: display cuts never change the stored key.
- **E13 (a `timeout_for` caller without a project root)**: passes `None` → 180. INVARIANT: a missing measurement never shortens a limit.
- **E14 (the off switch `skip_stand_limits`)**: no measurement, no note; readers see `none` (or an older live row). INVARIANT: an informed
  switch stays informed (FR-4); no config key becomes an error.
- **E15 (brief size, AR-20)**: no line on `none` and on the S5 plan dispatch, so the ratchet seed (no registry row) grows by 0 B; on a real
  run with a measurement each of the three briefs grows by one line of about 230 B (estimate: the line's fixed text is ~200 characters plus
  the address; the builder prints the measured line length from a test row). INVARIANT: a ratchet moves only by a named raise.
- **E16 (no e2e rows and no manual row; only handed profiles)**: nothing measured. INVARIANT: no browser opens for a number nothing uses.
- **E17 (two gate A runs at once)**: `record` runs under the registry lock (`project_knowledge.lock` :185); a busy lock → the note says it
  was not kept; nothing is lost. INVARIANT: two writers never lose a row.
- **E18 (two stands share the selected name)**: a note, no measurement, no record; the brief (`_stand_pick` → None) shows no line.
  INVARIANT: a doubt is never one stand.
- **E19 TEMPORAL (before j1 / after j1)**: before j1's first gate A on a project the registry holds no row (the file may not exist): every
  reader is `none` → 180 s, no brief line. The move that creates the row is the first `check_stand_page_load` on a project with a due
  use. A config with a hand-written `measured.e2e_page_load_s`: from j1 on it is no longer read; under the `max` rule the limit is never
  below 180 s, so only a hand value > 150 gave a longer limit before (none recorded, M5). INVARIANT: every limit comes from a measurement
  or the declared default, and none shrinks.
- **E20 (a no-trace story, P8/FR-53)**: measured, used in this rehearsal's note, NOT kept (`_refuse_no_trace`); the brief reads only what
  earlier normal runs kept. INVARIANT: a comparison run writes nothing into the project; its briefs differ from a normal run's only by what
  the project already holds (an ordinary condition named by the owner's principle P8, not an exception road: the write goes through the
  same `record`, which refuses).
- **E21 TEMPORAL (between j1 and j2)**: on one branch only — j1 and j2 merge in ONE wave with no release cut between (§E). Should a release
  be cut anyway, the old note "not measured" and the new measured note would contradict (FR-10), and `_stand_limit_card` / the two
  FACTORY_DEFECT cards would still fire for a config with hand values (V2 F11; none recorded, M5). INVARIANT: main never holds j1 without j2.
- **E22 (j2: a slow stand at the reporter)**: the `over` skip is gone; the reporter's own timeout and outcome states speak. INVARIANT: no
  step reads the deleted limit; the reporter's `timed_out` question is the sibling routed by F-j-reporter.
- **E23 (j2: projects that set `skip_stand_limits`)**: the key keeps one reader (`check_stand_page_load`), documented in the changelog and
  in `config-keys.json` `gate_rehearsal.needed_by`. INVARIANT: a project's existing switch keeps a meaning.
- **E24 (j2: delivery tests using the id `e2e_stand_limit` as sample data)**: untouched, a report line each. INVARIANT: no live code reads
  the deleted id.
- **Moot brief edges (from r1)**: `n/a`, the four `unmeasured` returns, `incomplete`, `unreadable` of the config record: all deleted in
  j2; successors E1, E2, E9, E10, E16, E19.

## §C. Small technical choices I closed

- No gate-registry row for the measurement: it judges no validity and nothing accepts or refuses on it.
- No delivery-report line: the number is not a story gap; a failure is told at gate A by its owner.
- The measurement code lives in `manual_capture.py` (it owns the backend, `stand_hosts`, `_safe_url`, `DEFAULT_TIMEOUT_S`) and the reader
  in `project_knowledge.py` (the registry's readers live there, precedent `sign_in`): no new module, so `test-layers.json` needs no
  `covers` change (V1 Fix 19 moot).
- `SOURCES` gains `"measured"` and `BY` gains `"gate"`: the honest provenance of a code measurement at gate A (not "role", not "driver").
- One registry subject per stand (`element: "frontend"`); `value` carries its own `at`, so each new measurement is a new row (the
  registry's "same value → existing row" rule :789 would otherwise keep an old `at`). Growth: at most one row per stand per 7 days plus
  definition/address changes (`show` lists them; `revoke` removes one).
- The unreadable registry case does not measure (the result could not be kept or read by any brief).
- `STAND_LOAD_ROLES` is a code set beside `FIRST_LOOK_KIND` (the factory's own wiring, same form). The S7 automator is not added (neither
  verdict asks; it would touch a fourth ratchet).
- `skip_stand_limits` keeps its name, no alias (V2 F10 optional part declined); the changelog and the catalogue state its meaning.
- Lazy imports in j1's new functions, so the `manual_capture.py:99-100` import line stays C3-k3's hunk.
- The address is cut at 120 characters for display.

## §D. Forks (returned, not decided)

- **F-j-store — where the measurement lives (the verdicts DISAGREE).** V1 Fix 2 / K6: a separate file breaks P31/AR-14/AR-25 (a third
  store beside the answer registry, no lock, no way out). V2 K3: AR-13/AR-14 "kept" with a separate file; F8a asks only a lock or a stated
  "last writer wins".
  - (a) **Recommended**: the answer registry (`environments.page_load`, `project_knowledge.record`/`page_load`). It is the one road for a
    stand fact the factory learns (precedent `environments.sign_in`, a machine-found fact), and it brings the lock (E17), `revoke` (AR-25),
    the unreadable/schema handling and — not named by either verdict — the no-trace refusal (P8/FR-53, E20) for free. Cost: edits in
    `project_knowledge.py` (two constants, one value-shape branch, one reader), one catalogue row, the FIVE_KEYS pin.
  - (b) A separate `records/stand-page-load.json` on `environment_record.load_rows/write_rows` with `schema_version`, a lock, a revoke door
    and a no-trace check — re-building what (a) has; AR-14/AR-25/P31 then need a written reason the registry does not fit. Not recommended.
  - The card is written for (a).
- **F-j-failed — is a failed measurement kept (the verdicts DISAGREE).** V1 Fix 3: never record `failed`; retry each gate A. V2 F7: a
  factory-side failure (`BrowserUnavailable`, launch error) IS reused; a stand-side failure is not.
  - (a) **Recommended**: never record any failure. "No browser" is a fact of ONE machine; recorded in a carried file it would stop a
    colleague's machine that has a browser (AR-4). Retrying costs an instant `ImportError` on a browserless machine. Under F-j-store (a)
    the registry stores only `known` rows anyway.
  - (b) V2's split: reuse factory-side failures. Saves nothing measurable; carries the AR-4 defect.
  - The card is written for (a). Both verdicts agree on the owner split of the texts (V1 Fix 5 = V2 F7 first half): applied.
- **F-j-reporter — the sibling question (V1 Fix 21; V2 E14/K2 names the same class).** `gate_preflight.py:3635-3641` asks a person to
  "raise `gate_rehearsal.reporter_timeout_s`" — a number they cannot know (the owner's second word). After j2 it is the reachable successor
  of the deleted skip.
  - (a) **Recommended**: a new rules-debt node after j2 (plan critic first: a person-asking card changes meaning): the reporter's one-test
    timeout is `max(reporter_timeout_s, measured load + margin)` and a timeout is REPORTED (note; the profile's report "unproven"), not
    asked. It may wait for the owner's F-home answer. Lead move: a line in the batch's «Остатки» `reporter timed_out card asks a person for
    a timeout | узел: <new id, rules-debt>`.
  - (b) Fold it into j2 now: widens j2 into a third meaning change without its own plan critic. Not recommended.
- **F-j-route2 — a signed-in sample (V2 K7 "zero-cost improvement", not blocking).** `sign_in` already returns the signed-in landing time
  (V2 cites `manual_capture.py:3030-3031`; I did not read those lines).
  - (a) **Recommended**: keep the Lead's route decision — signed-in load is a later node; j1 stays signed-out with floor wording.
  - (b) j1 also records the sign-in probe's landing time as a second sample: more value for cmp2-like stands, but it only exists when a
    manual case has an account, and it widens j1 (another writer path, another shape).
- **F-j0 / route (a) check (brief: "if a finding shows (C) or route (a) cannot hold, fork").** V2 K7 shows a signed-out load is the WRONG
  number as a CEILING (it shortens limits → a person is asked, F2) and is likely below the cmp2 editor's load (estimate, not verified). It
  is a right number as a FLOOR. With F2 applied (`max(180, load+30)`, floor wording), (C) and route (a) hold; nothing to re-decide unless
  the Lead takes F-j-route2 (b).
- **F-home — where the owner's stand principle lives (for the owner; nothing is placed).** The corrected texts of V1 K9, to show her:
  - P32 (proposal): «Любой стенд, который нам дали, — готовый тестовый стенд, пока человек не скажет иного. Чего не хватает (например,
    доступа), фабрика спрашивает — как это получить; если человек говорит, что на этом стенде этого нет вовсе, фабрика принимает это и
    может предложить моки. Число о стенде, которое нужно работе (например, время загрузки страницы для ожиданий в тестах), фабрика
    измеряет сама и использует; человека о нём не спрашивают — он его не знает. Понятие, которое никому не нужно, удаляется.»
  - FR-50 sentence (proposal): "A stand the factory is given is a ready test stand unless a person says otherwise. What the work is missing
    on it (an access) is asked as how to get it; when the person says the stand does not have it at all, that is accepted and mocks may be
    offered. A number about the stand that the work uses is measured by the factory and used; a person is never asked for it."
  - Say to the owner: "a number they cannot know" generalises «этот лимит … точно не знает» (V1 K9). Options: (a) both P32 and the FR-50
    sentence (recommended); (b) P32 only. Placement is the owner's / the architect's; j1 and j2 do not wait for it.

## §E. Serial order and file overlap with the other wave-3 cards (read this round)

Read: k r2 §0.1-§0.2 (:21-43), owns of k2 (:451-459), k3 (:575-585), k4 (:713-722); conversions r2 §4 (:554-590); g-h r2 grep of shared
names (census lines :205, :528, :683 are non-goals); batch `plans/piles/rules-debt/batch-1-phase-2.md` :10, :39-42.

The contradiction V1 K5 found: r2 §E put j before k (`C3-rr → C3-j1 → C3-j2 → C3-k2 → C3-h`), while k r2 §0.1 removed C3-j from both
queues and made it the later merger. Resolved FOR the k r2 order (V1 Fix 15 = V2 F8b, both verdicts agree):

| shared file | who writes it | order |
|---|---|---|
| `gate_preflight.py` (HOT) | k2 (`_observed_identity`, :87, `_reporter_outcome`), C3-h (queue line only), j1, j2 | C3-k2 → C3-h → C3-j1 → C3-j2 |
| `test_gate_preflight.py` | k2 (stub :4261, K30 row), j1, j2 | k2 → j1 → j2 |
| `manual_capture.py`, `test_manual_capture.py` | k3 (`stand_probe`, import :99-100; rows `stand_probe`), j1 | k3 → j1 (function-disjoint; j1 is the later merger, re-runs its rows) |
| `judgment-census.json` | k4 (row :826 only if asked), j1 (one row), j2 (row :418) | k4 → j1 → j2 (row-disjoint). Neither g-h r2 nor conversions r2 writes it (V2 F8b is right; V1 K5 "written by g-h r2 … and conversions r2" is not borne out by the cards' owns: closing table) |
| `gate-registry.json`, `test_gate_registry.py` | C3-g, RD1-26+28, RD1-29, k1-k4, C3-h, j2 | `C3-g → RD1-26+28 → RD1-29 → C3-k1 → C3-k2 → C3-k3 → C3-k4 → C3-h → C3-j2` (conversions r2 :582 plus j2 last); j2 re-derives its pins as deltas (S-f) |
| `config-keys.json` | j1 (rows), j2 (two entries) | j1 → j2 (row-disjoint); no other wave-3 card owns it (Grep of the three r2 files: 0 owns lines) |
| `brief_pack.py`, `project_knowledge.py`, `investigation_probe.py`, `walk_session.py`, `references/manual-evidence.md` | j1 only among wave-3 cards (k4 greps `manual-evidence.md` for prose, edits only inside its owns) | — |

Rules: j1 is built from main after C3-h has merged (or merges main in as the later merger); j2 is built on j1's branch; **j1 and j2 merge
into main in ONE `wave.py merge` wave, and no release is cut between them** (FR-10, E21). Zone overlap with batches of OTHER piles in work
for the new j1 files: `python tools/piles.py check` — the Lead's door before dispatch (V1 trail "Not done").

Lead moves before the j1 dispatch (V1 Fix 16; the Lead's carriers, not a builder's):
1. Batch row RD1-13 (`batch-1-phase-2.md:41`), «Что»: «метка спеки: RD2-C3-j; направление (C) (слово владельца 17.11.2026): фабрика
   измеряет загрузку стенда на гейте A и отдаёт её ролям (узел j1), ожидание page objects и сравнение кодом удаляются целиком (узел j2);
   ни одна ветка не спрашивает человека; карточка `docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md`»; «Пишет в»: j1 and j2 owns of
   this card; «Зависит от»: «RD1-11 (C3-h) и цепочка C3-k1…k4 (поздний мерджер по `gate_preflight.py`, `manual_capture.py`,
   `judgment-census.json`, `gate-registry.json`); j1 и j2 сливаются одной волной».
2. The same file: the order line :10 (`C3-i → C3-j → C3-k → C3-h`) → `C3-i → C3-k → C3-h → C3-j`; RD1-11 «Зависит от» (:39) and RD1-14
   (:42, «RD1-13 (C3-j) (очередь `gate_preflight.py`, третья)») lose C3-j.
3. Finding `plans/piles/rules-debt/findings/20261117-rd2-c3-j-s5-stand-limits-otvet-v-reestre.md`: a head line «заменено карточкой C3-j r3
   (слово владельца 17.11.2026)».
4. If the batch is taken by then, the edits follow `docs/TEAMWORK.md` §2 (a taken batch).

## §F. The measured premise (M5, t-1092)

t-1092 decoded `state/config-at-start.json` of the three recorded stories with a config (cart-1, local-1-0108, local-1-arm-b): profile
`web` has no `page_object_max_wait_s`, environment `local` has no `measured`; e2e-ui rows 1/10, 13/21, 10/17 → `_e2e_limit` is
`unmeasured` on 3/3. Reproduce (not run here): `python -B -c "import json,base64,glob;[print(p,[(x.get('profile_id'),x.get('page_object_max_wait_s')) for x in c.get('profiles',[])],[(e.get('name'),(e.get('measured') or {}).get('e2e_page_load_s')) for e in c.get('environments',[])]) for p in sorted(glob.glob('C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/state/config-at-start.json')) for c in [json.loads(base64.b64decode(json.load(open(p,encoding='utf-8'))['bytes_b64']).decode('utf-8-sig'))]]"` → expected three lines with `('web', None)` and `('local', None)` (a printed profile id is the positive control).

## §G. Readers of every touched file (rule 7)

Searches this round: Grep count over `C:/QAFactory/forge-repo/tools`, pattern `project_knowledge|config-keys|investigation_probe|walk_session|manual-evidence\.md|test-layers\.json` → 41 hits in 12 files; r2's grep over `tools/` for `gate_preflight|gate-registry|manual_capture|brief_pack|judgment-census|...` → 19 hits in 6 files; over `.githooks/` for all touched names → 1 hit (`commit-msg`); over `.claude/` → the search descended into `.claude/worktrees/*` (other sessions' repo copies, not readers) and timed out: readers in `.claude/agents|hooks|settings` NOT established (gap, named; the Lead runs `Grep` with `glob` `!.claude/worktrees/**` before dispatch).

| touched file | readers outside the package | verdict |
|---|---|---|
| `references/gate-registry.json` (j2) | `tools/source-split-carriers.json:15, :35`, `tools/source_split.py`, `tools/test_quarantine.py:2199` | unchanged (row form unchanged) |
| `judgment-census.json` (j1, j2) | `tools/architecture_gate.py:88` (`CENSUS_REL`), `tools/source-split-carriers.json`, `.githooks/commit-msg` (via the gate) | j1/j2 read its census rule before the commit; form unchanged |
| `references/config-keys.json` (j1, j2) | hits among the 12 files (not read per hit; candidates `tools/owns_readers.py`/`owns_readers.json`, `tools/test_owns_readers.py`) | unchanged: no key renamed, one row of an existing form added; the builder reads `tools/owns_readers.py` and reports one line |
| `project_knowledge.py`, `manual_capture.py`, `brief_pack.py`, `gate_preflight.py`, `investigation_probe.py`, `walk_session.py` (j1) | `tools/source_split.py` strings, `tools/test_forge_metrics.py:432, :438` (brief_pack path sample), `tools/test_piles_split.py:86` (glob string) | unchanged: no file renamed |
| `references/manual-evidence.md` (j1) | none found among the hits named | unchanged |
| `scaffold.py`, the four test files (j1, j2) | `tools/test_quarantine.py`, `tools/test_redundancy.py`, `tools/test_split.py`, `tools/lint_ratchet.py` read test files and `test-layers.json` by name | unchanged: no test file added, renamed or moved between layers |
| package readers of the changed names | `timeout_for` (8 call sites, j1), the deleted functions (j2: only gate_preflight and its tests, plus two delivery tests' sample ids), `measurement_is_stale` (j1 delegate, j2 delete), the catalogue `needed_by` (j1 adds, j2 removes) | change in j1 / j2 as listed |

## Closing table — every fix of both verdicts → where applied in r3

| fix | verdict | applied where | note |
|---|---|---|---|
| Fix 1 (callers in owns) | V1 | §2 owns, item 2 | same as V2 F1 (a) |
| Fix 2 (one store) | V1 | §2 item 1, §1 AR-3/14/25 | disagrees with V2 K3 → fork F-j-store, written for (a) |
| Fix 3 (failed never recorded; REUSE_DAYS 7) | V1 | §2 items 1 (step 9), 3 (step 6); E3, E7, E9 | disagrees with V2 F7 reuse half → fork F-j-failed, written for (a) |
| Fix 4 (no web page → n/a) | V1 | §2 item 2 steps 2-3; E2 | the trigger stays "e2e-ui row or any manual row" (a manual capture always takes its limit from `timeout_for`); the stand-side `n/a` removes the false failure; a web stand with only http manual cases pays one load per 7 days (AR-12, named) |
| Fix 5 (cause classes) | V1 | §2 item 2 step 5-6, item 3 texts | = V2 F7 first half |
| Fix 6 (userinfo) | V1 | §2 item 2 step 4, item 1 faults; E11 | |
| Fix 7 (duplicate names) | V1 | §2 item 3 step 3; E18 | |
| Fix 8 (one staleness body) | V1 | §2 item 1 `stale_against_verified`, item 3 delegate; §3 owns | makes V2 "acceptable copy" moot |
| Fix 9 (anchors) | V1 | §2 item 2 (goto, StepTimeout/StepFailed, `definition_sha_for(cfg, name)`, 210), item 3 (lifted trigger), item 4 (`_stand_pick` `[1]`) | = V2 F9 |
| Fix 10 (roles) | V1 | §2 item 4 `STAND_LOAD_ROLES` | |
| Fix 11 (census row in j1) | V1 | §1 table, §2 item 5, owns | V2 "not established" resolved by `test_judgment_census.py:17-19` (u1) |
| Fix 12 (carrier of the waits judgment) | V1 | §1 table, option (a) | |
| Fix 13 (catalogue) | V1 | §2 item 5, §3 owns | = V2 F6 |
| Fix 14 (j2 deletions whole) | V1 | §3 item 4 | |
| Fix 15 (§E order) | V1 | §E | = V2 F8b |
| Fix 16 (one carrier) | V1 | §E Lead moves 1-4; one Lead-decisions block below | the batch and the finding are Lead carriers, not a builder's owns |
| Fix 17 (window, FR-10) | V1 | §E rule, E21 | wave invariant chosen (V1's recommendation) |
| Fix 18 (test lines, trimming) | V1 | DoD `test:` lines; §2 item 6 "Not written" | |
| Fix 19 (test-layers covers) | V1 | §C | moot: no new module under F-j-store (a) |
| Fix 20 (scaffold, real browser) | V1 | §2 items 5-6; default stub; the 45-file count and the info-pin grep | "keep 100 s via a recorded 70" is moot under V2 F2 (`max(180, …)`): expectations move to 180 s; the round trip is proved by the 160 → 190 rows |
| Fix 21 (reporter timeout sibling) | V1 | §D F-j-reporter | another node: returned as a fork |
| Fix 22 (F-home texts; §0 whole quote) | V1 | §0, §D F-home | |
| F1 (callers) | V2 | §2 owns, item 2 | (a) taken |
| F2 (floor, never shortens) | V2 | §0, §2 item 2 `max`, item 4 wording, item 5 manual-evidence.md; E6, E13, E19 | |
| F3 (brief bytes) | V2 | §2 item 4 (no `none` line, no plan dispatch), DoD (3), E15 | (iii) named raise only if a ratchet moves (expected 0 B) |
| F4 (scaffold / landing_limit) | V2 | §2 item 6 (moved expectations), item 5 | |
| F5 (address in the key) | V2 | §2 item 1 step 8; E9 | |
| F6 (config-keys) | V2 | §2 item 5, §3 owns | = Fix 13 |
| F7 (owner split, retry) | V2 | texts applied; reuse half → F-j-failed | |
| F8a (concurrent writers) | V2 | E17 (registry lock) | under F-j-store (b) a lock is required in the file road |
| F8b (§E stale) | V2 | §E | V2's census claim confirmed, V1's "g-h and conversions write the census" not borne out |
| F9 (lookups, `_safe_url`) | V2 | §2 item 2 | |
| F10 (`skip_stand_limits` meaning) | V2 | §2 item 7, §C, E14, E23 | alias declined (small choice) |
| F11 (window residual) | V2 | E21 | |
| K7 zero-cost signed-in sample | V2 | §D F-j-route2 | |

Counts: 33 fix items (V1 22 + V2 11); applied 29; returned as forks 4 (F-j-store, F-j-failed, F-j-reporter, F-j-route2) — of which the
two disagreements are written for the recommendation, so the card is executable before the Lead answers.

## Lead decisions that stand (one block; the duplicate r2 block is dropped, V1 Fix 16)

From r2 (architect-rank session, 17.11.2026; by recommendation, until the owner's word): F-j0 = (C); F-j-route = (a), the signed-in load a
later node; F-j-split = (a), j1 then j2, serial; F-j-defects moot under (C); F-home NOT decided by the Lead — shown to the owner, j1/j2 do
not wait. Plan critics t-1123 (two reports, both standing) → this fix round t-1132.

## Reading trail

- Given, whole: card r2; V1; V2. k r2 :1-120, :445-464, :570-589, :706-729 and a grep of shared names; conversions r2 :555-584 and grep;
  g-h r2 grep; batch `batch-1-phase-2.md` whole.
- `project_knowledge.py` :1-130, :174-253, :265-354, :440-525, :586-603, :626-812 (+ def list); `first_look.py:1002-1042`;
  `external_writes.py:191-203`.
- `gate_preflight.py` :150-211, :2685-2830, :3085-3345, :3628-3645, :6060-6110 (+ greps: helper defs, `reporter_timeout_s|timed_out`,
  `stand limit|page load|measured`).
- `manual_capture.py` :95-120, :545-574, :1640-1824 (+ greps of `StepFailed|StepTimeout|BrowserUnavailable|BACKEND_FACTORY|_safe_url|
  stand_hosts|host_key|sign_in|await_landing`).
- `env_probe.py` def greps (:383-396, :421-427, :449-463, :535-549); `stand_identity.py` :129-154.
- `brief_pack.py` :2730-2749, :2878-2895, :3378-3408, :4130-4154, :4520-4574 (+ greps `SIDES_ROLES|s5_plan|TIMEOUT_ROLE`).
- `config-keys.json` :700-744; `manual-evidence.md` grep (:57); `judgment-census.json` :1-8 + grep; `test_judgment_census.py` :1-45.
- Tests: `test-layers.json` :288-312, :3010-3033, :4112-4136 (+ grep of four keys); `test_brief_pack.py` :2395-2443; `S5_PLAN_BRIEF_BYTES_MAX`
  grep; `scaffold.py` :40-89; `test_manual_capture.py` grep of the 100-s expectations; `test_gate_preflight.py` :30-64, :2143-2262,
  :6018-6046, def list, stand-limit grep; `test_project_knowledge.py` KEYS grep; `test_gate_role_accounts.py` :285-302; `harness.py` greps.
- `docs/TESTING.md` :36-95.
- Searches with controls: named in §A, §2 item 6, §G. Not read: `manual_capture.py:3005-3031` (V2's `elapsed_s`), `investigation_probe.py`
  and `walk_session.py` around the calls (V1/V2 read them), `test_gate_registry.py` pins (carried from r2), the runner block :6200-6290 of
  `test_gate_preflight.py` beyond the five grep lines (j2 item 4 makes the builder find every name), `tools/owns_readers.py`, `.claude/`
  outside worktrees (rule 7 gap, §G).

## Lead decisions on r3 (architect-rank session 501cb4e0, 17.11.2026; by recommendation, until the owner's word)

- F-j-store = (a) the answer registry (one store, its lock). F-j-failed = (a) a failed measurement is never kept.
- F-j-reporter: a new node of the rules-debt pile (the reporter's timeout sibling), opened by the Lead after j2; it does not
  hold j1/j2. F-j-route2 (a signed-in sample): later, not opened now.
- F-home: the owner decides (the K9 texts are with her).
- No third plan critic: 29 of 33 fixes applied as written, the direction (C) is unchanged; the code critic judges j1 and j2
  (one pass for the topic).
- Dispatch: j1 then j2, after the C3 wave is on main.
