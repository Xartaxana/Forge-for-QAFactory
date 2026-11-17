# t-1123: plan review of card C3-j r2 (RD1-13, F19)

**VERDICT: GO WITH FIXES.** 4 findings must be fixed before the j1 dispatch (F1-F4), 4 medium (F5-F8), 3 low (F9-F11).
The direction (C) holds. The plan has two problems as written. First, j1's new `timeout_for` lets a signed-out landing
time SHORTEN every manual-capture limit and the gate's sign-in probe from today's 180 s, which opens a path that asks a
person (K2). Second, j1 cannot be built inside its owns: two callers of `timeout_for` sit outside them, and so do a test
fixture and two brief ratchets the change breaks. Every fix is an edit to the card; no redesign is needed. The decision
to accept stays with the Lead.

Base: root checkout `main` at b89871b3 (the card read 9a7acdf3; the files named below did not move for the lines quoted).

## Keys

- **K1 FACTS: FIX.** The negative claim holds. I ran a case-insensitive Grep for `page_object_max_wait_s|e2e_page_load_s` over the
  whole package, tests included. No producer exists in the shipped code. The positive control is the same call, which finds
  `gate_preflight.py:3118-3121`. The readers named in §A are correct: `_e2e_limit` :3089, `check_s5_stand_limits` :3166,
  the reporter skip :3323-3330, `_stand_limit_card` :3243/:3250 and `timeout_for` :555-562. But the reader list of
  `timeout_for` is incomplete (F1). A test fixture that DOES write the key was missed (F4). A config doc carrying the deleted
  function names was missed (F6).
- **K2 OWNER'S WORD: FIX.** j1's own texts ask nothing, and neither does a failed measurement (note only; FR-3 kept). But j1
  item 3 opens a path that does ask, through the sign-in probe (F2). The j1→j2 window keeps today's `over` card and its
  FACTORY_DEFECT cards for any config that carries hand values (F11, low: M5 shows none recorded).
- **K3 ARCHITECTURE: FIX.**
  - Kept: AR-22, AR-13 and AR-14 (one writer `record`, one reader `read`), AR-29 and AR-20 (census shrink named in j2).
  - AR-4 is incomplete: the key leaves out the address actually measured (F5).
  - AR-28/FR-41/FR-59 are violated in the timeout direction (F2).
  - AR-11/AR-12/AR-20: j1 adds bytes to briefs at their ratchets and the card names no payment (F3).
- **K4 EDGES: FIX.** These have no stated behaviour, or the wrong one:
  - an unreachable or down stand: it is recorded as `failed`, reused indefinitely and called "a defect of the factory" (F7);
  - two concurrent writers of the record (F8);
  - an address from the env file changing under the same `definition_sha` (F5);
  - a redirect to an off-stand sign-in host (F7);
  - the meaning of `skip_stand_limits` changing (F10).

  Covered adequately: E1-E5, E9-E11, E16, a stale record (E8), a profile with no e2e rows (E10), no headless browser (E3).
- **K5 DELETION COMPLETENESS (j2): FIX.**
  - Named and correct: the functions, registry row :480, census row :418, `NEW_CHECK_FUNCTIONS` :3651, FR-6 scan :3809,
    selftest lines :6394/:6398, `run` tuple :6089, docstrings :57/:804.
  - Missing: `references/config-keys.json` `needed_by` lists `gate_preflight.py:check_s5_stand_limits` under `profiles`
    (:724) and `gate_preflight.py:_stand_limit_card` under `environments` (:733) (F6).
  - The old keys are inert after j2 (no reader is left). The card states that config files carrying them are unaffected:
    PASS on that part.
- **K6 EXECUTABILITY: FIX.**
  - Owns gaps: F1, F3, F4.
  - The "STOP if the backend has no navigation call" clause can be resolved now. `PlaywrightBackend.goto(url)` exists at
    `manual_capture.py:1814`: it returns elapsed seconds with `wait_until="load"`, and on a timeout `_timed` raises
    `StepTimeout(elapsed)` (:1801-1812) (F9).
  - Sibling-card conflicts: §E is stale against the k-cards r2 (F8b).
  - Witness scope: narrow, acceptable.
- **K7 FEASIBILITY: PASS with F2.**
  - The instrument exists: `_probe_sign_in` (`gate_preflight.py:2803-2811`) already does `BACKEND_FACTORY()` or
    `PlaywrightBackend()`, then `open(timeout, stand_hosts)` and `close` in `finally`. `goto` adds the timed navigation.
  - A signed-out load is honest ONLY as a lower bound. The cmp2 lesson the card cites (`gate_preflight.py:3104-3105`) was "a
    full load of the workflow editor took 70-110 s under Vite dev": a signed-in deep route, served module-on-demand. A
    signed-out landing on the same stand can load in seconds. So route (a) would likely NOT have caught cmp2. This is
    "estimate, not verified": no run exists either way.
  - (C) is still the right reading of «надо измерить и использовать» for the automator's brief, as long as every text calls
    the number a floor.
  - For `manual_capture.timeout_for`, (B) is the truer reading: keep 180 s and let the measurement only LENGTHEN it (F2).
  - The Lead's F-j0 = (C), F-j-route = (a) and F-j-split = (a) stand, with F2 applied.
  - Zero-cost improvement, recommended but not blocking: `sign_in` already returns the signed-in landing time
    (`manual_capture.py:3030-3031`, `elapsed_s`). Recording it as a second sample when `check_actor_sign_in` runs gets part
    of route (b) for free.

Standing questions:
- **DUPLICATION AND CONSISTENCY: one finding.** `is_stale` is copied during the j1→j2 window, named in E13 and removed in j2:
  acceptable. I grepped `def measurement_is_stale|limit_seconds` and found one definition each in `gate_preflight.py`, with
  no other caller (`cost_capture._limit_seconds` is unrelated). New duplication found: none.
- **CODE QUALITY: none found.** Plan only. I checked the signatures of the reused functions:
  - `stand_identity.definition_sha_for(cfg, environment_id: str)` takes a NAME, not the stand dict the card writes
    (`definition_sha_for(cfg, stand)`, §2 item 1). This is part of F9.
  - `env_probe.frontend_of(...)` returns a dict; the address is its `["url"]`.
- **ONE ROAD (P31): PASS.** The measurement sits at gate A, which both roads reach: `driver_gates.py:120` runs
  `gate_preflight.py --gate A`, and `skills/qa-story/phases/s4.md:19` tells the skill road to rehearse it. No language,
  project or case is excluded.
- **TESTS: FIX.** The rows are in existing keep tables (good). Four existing tests break and are not named: the K5
  `landing_limit` rows, two brief ratchets and the S5 plan ratchet (F3, F4).

## Findings

### Blocking (fix before dispatch)

**F1. The signature change of `timeout_for` breaks callers outside j1's owns.** Where: card §2 item 3 and the j1 owns.
- The card changes `timeout_for(env)` to `timeout_for(project_root, cfg, stand)` and names only `gate_preflight.py:2808`,
  `manual_capture.py:3413` and "the :5430-5445 region".
- The real call sites, by my case-insensitive Grep (positive control: the definition at `manual_capture.py:555`):
  - `manual_capture.py:3015` (`sign_in`), :3178 (the ui capture), :3413 (the app capture) and :5383 (the http call);
  - `investigation_probe.py:419`;
  - `walk_session.py:1221`;
  - `gate_preflight.py:2808`.

`investigation_probe.py` and `walk_session.py` are NOT in owns, so after j1 those two calls raise TypeError. The card's
"edit outside owns is a question" applies only to the prose siblings.

Fix, either of two:
- (a) Add `scripts/investigation_probe.py` and `scripts/walk_session.py` (the call line only) to j1 owns, with a report line
  per hit. Both have `cfg` and a project root in scope: `investigation_probe.py:416` `cfg, project = MC.load_config(task)`,
  and `walk_session.py` `self.cfg` / `self.project_root`.
- (b) Keep the one-argument form readable: `timeout_for(stand, *, project_root=None, cfg=None)`, where absent root or cfg
  means `DEFAULT_TIMEOUT_S`.

(a) is cleaner (AR-13: no caller silently keeps the default).

**F2. A signed-out landing time shortens every manual limit and the gate's sign-in probe. That opens a path that asks a
person.** Where: §2 item 3, E12, E14.
- Today nothing produces the key, so every story gets 180 s.
- Under j1, a stand whose signed-out landing loads in 2 s gives `load_s + 30` = 32 s to every caller in F1. That covers the
  signed-in landing of `sign_in`: `await_landing(backend, recipe, hosts, timeout_s)` at `manual_capture.py:3021`, fed by
  `timeout_s or timeout_for(stand)` at :3015. It also covers the http calls (:5383) and the app capture (:3413).
- The trace on a cmp2-like stand (signed-out login page fast, signed-in landing 70 s):
  1. The first gate A runs `check_actor_sign_in` before `check_stand_page_load`, so it still uses 180 s (E14). It records the
     2 s measurement.
  2. On the next rehearsal, or any story on that stand (the record is project-level), `_probe_sign_in` opens with
     `MC.timeout_for(stand)` (`gate_preflight.py:2808`) = 32 s.
  3. `await_landing` gives up at 32 s and returns `not_landed`.
  4. `check_actor_sign_in` then raises `self.add(check, PERSON_DECIDES, "... the stand did not let it in ...")`
     (`gate_preflight.py:2788-2792`).

So a person is asked about a stand the factory itself cut short. This breaks K2, AR-28 (a number that describes something
else becomes a limit) and the card's own E12 "safe direction".

Fix: `timeout_for` → `max(DEFAULT_TIMEOUT_S, load_s + TIMEOUT_MARGIN_S)` when `measured`, else `DEFAULT_TIMEOUT_S`. The
measurement may only lengthen a limit. Then:
- the test rows flip to: recorded 70 → 180, recorded 160 → 190, `at_least` 180 → 210;
- E12's invariant becomes true as stated;
- `references/manual-evidence.md:57` ("the stand's measured page load + 30 s (else 180 s)") becomes "180 s, or the measured
  page load + 30 s when that is longer". That edit is in j1 owns, as an FR-37 text a role reads.

In the brief line, say "at least" in spirit: "the landing page loads in X s signed out; pages behind the sign-in can be
slower". Replace "Page-object waits are written to fit it" with "fit your waits to the slowest load your own runs show,
never below this".

**F3. j1 adds bytes to briefs that sit at their ratchets, and the card names neither the cost nor the payment.** Where: §2
item 4, E1, j1 owns.
- `STAND_LOAD_ROLES` includes `("S5","qa-code-critic")`. The S5 PLAN critic brief is built as
  `brief_pack.build(TICKET, "S5", "qa-code-critic", "S5-plan-critic-1")` (`test_brief_pack_s5_plan.py:38, :73-74, :591`).
- E1 says the line appears even with no stand ("not measured yet", 36 B + newline). So the plan brief gains it, and
  `S5_PLAN_BRIEF_BYTES_MAX = 9559` (:542) is the brief the Lead reports as exactly at its ceiling. That file is not in j1
  owns.
- `ROLE_BRIEF_BYTES_MAX` (`test_brief_pack.py:2411-2415`) also gets +36 B or more for `qa-automator` 6863, `qa-code-critic`
  7189, `qa-runner` 5670 and `qa-failure-analyst` 6442 (the Lead reports margins of 1-8 B).

Fix:
- (i) No line when no stand is selected, or when nothing at gate A would have measured: no e2e rows and no manual case,
  E10/E11, AR-11. The "none" line appears only when a measurement was due.
- (ii) Leave the S5 plan dispatches out (purpose `s5_plan`): the plan author and critic write no waits.
- (iii) For what remains, name the AR-20 raise per role in `ROLE_BRIEF_BYTES_MAX` with a RAISE comment line (measured at
  build, a delta). If any plan brief still grows, add `test_brief_pack_s5_plan.py` (the ratchet line only) to owns.

**F4. A test fixture writes the old key, and the test that leans on it breaks.** Where: j1 owns and item 5.
- `scripts/tests/fixtures/manual-evidence/scaffold.py:68` puts `"measured": {"e2e_page_load_s": {"value": 70, ...}}` into
  the shared manual-evidence config.
- `test_manual_capture.py:1467` pins `LANDING_LIMIT = 100  # make_task's stand: measured page load 70 s + 30 s`.
  `landing_limit()` (:1657-1674) expects poll 401 (100.25 s) to fail with exit 3 through `landing_run`, which takes the limit
  from `timeout_for`. After j1 the limit is 180, so the landing at 100.25 s succeeds and K5 goes red.
- The card's E12 fixture grep searched only the note text and the check id, so it missed the key.

Fix:
- Name `landing_limit` and `LANDING_LIMIT` in j1's test edits. Either seed a `stand_load` record of 70 into the scaffold
  project, or set `LANDING_LIMIT = 180` and keep the AT/BEYOND pair.
- Delete the dead `measured` block from `scaffold.py` (add it to owns), or say why it stays.
- The builder greps every scaffold-based test for a 100 s assumption and gives a line per hit. Their count is "not
  established" here.

### Medium

**F5. AR-4/E8: the key leaves out the measured address.**
- `frontend_of` can take the address from the env file (`values`, the block's `url_key`) and from a derived base address
  (`env_probe.py:454-458`). Neither is part of `definition_sha(entry)` (`stand_identity.py:149-154`).
- If the env-file address changes, the old measurement of another host still "speaks for this one". That breaks E8's own
  invariant.

Fix: `read` returns `none` when the row's `address` differs from today's `frontend_of(...)["url"]`. Add one test row.

**F6. j2 leaves stale reader lists in `references/config-keys.json`.**
- `needed_by` names `gate_preflight.py:check_s5_stand_limits` under `profiles` (:724) and `gate_preflight.py:_stand_limit_card`
  under `environments` (:733). Both functions are deleted in j2. No test checks that the names exist (Grep `needed_by` over
  `scripts/`: only `test_config_migration.py:400-407`, which checks shape), so the drift would be silent.
- j1 adds a new reader of `environments` (`stand_load.read` / `measure` via `frontend_of`, `definition_sha_for`).

Fix: add `config-keys.json` to j2 owns (remove the two entries) and to j1 owns (add `stand_load.py:read`, `stand_load.py:measure`).

**F7. The failure owner and retry are wrong for stand-side failures.**
- `measure` maps "any exception" to `failed`, and every failed text says "a defect of the factory". An unreachable stand, a
  stand that is down, or a redirect to an IdP host outside `stand_hosts` (the route guard aborts it,
  `manual_capture.py:1676-1684`, so `goto` raises `StepFailed`) is the stand's state, not the factory's. FR-19 and AR-27:
  the owner must be right.
- A `failed` row is then REUSED until the definition or `verified` changes (§C). One moment of downtime leaves the stand
  "not measured" for good.

Fix: split `failed` by owner. `BrowserUnavailable` or a launch error is the factory's and is reused. `StepFailed` from the
navigation is the stand's: it is not reused, and the next rehearsal measures again. The texts name the owner. Add rows for
both.

**F8. Concurrent writers and sibling-card order.**
- (a) Two gate A rehearsals on one project can each read, measure and `record` the WHOLE file. The last `atomic_json` wins,
  and a row for another key written in between is lost. That is mild (it is re-measured), but the card has no edge for it.
  Fix: name the edge, and either take the package's file lock around read-modify-write (a `file_lock` module exists; see
  `test_file_lock.py`) or state "last writer wins; a lost row is re-measured" as the accepted behaviour.
- (b) §E is stale. `20261117-rules-debt-wave3-k-cards-r2.md` §0.1-§0.2 (:25-43) REMOVED C3-j from both queues: the HOT
  queue is now `C3-k2 → C3-h`, and the registry queue is `C3-g → k1 → k2 → k3 → k4 → C3-h`. It says "if C3-j lands later, it
  is the later merger, re-derives its pins and re-measures D13". It also writes files j1/j2 touch:
  - C3-k3 owns `manual_capture.py` (`stand_probe` :1612-1613, the import line :99-100) and `test_manual_capture.py` (rows
    `stand_probe`). That is function-disjoint from j1's `timeout_for` and callers, but it is the same file.
  - C3-k4 owns `judgment-census.json` (row :826), which is row-disjoint from j2's :418.
  - Neither g-h r2 nor conversions r2 writes `brief_pack.py`, `manual_capture.py` or `judgment-census.json`. Their census
    mentions are "unchanged" or non-goals (Grep, case-insensitive, over the three files).

  Fix: rewrite §E. j1 and j2 enter after the k-chain on `gate_preflight.py`, or before C3-k2 only if the Lead re-orders
  the k-cards. On `manual_capture.py` and `test_manual_capture.py`, whichever of j1 and k3 lands later merges main and
  re-runs its rows. j2 re-derives its registry pins as the later merger (S-f).

### Low

**F9. Resolve the card's open lookups now.**
- `goto` exists (`manual_capture.py:1814`) and returns seconds. `StepTimeout(elapsed)` is the timeout → `at_least`, and it
  must be caught BEFORE the generic handler.
- `definition_sha_for(cfg, stand["name"])`, not `(cfg, stand)`.
- The address is `frontend_of(cfg, name, root=project_root)["url"]`.
- Store and print the address through `manual_capture._safe_url`, the same as the session lines.

**F10. `skip_stand_limits` changes meaning.**
- It used to mean "do not compare", and after j2 it means "do not measure". E17's "keeps a meaning" is true only loosely,
  and after j2 the key's name refers to a concept that is gone.
- Fix: one sentence in the changelog fragment on the new meaning. Optionally, accept a new key `skip_stand_page_load` that
  reads the old one as an alias. Document whichever is chosen in config-keys.

**F11. The j1→j2 window still has person cards.** In that window, `_stand_limit_card` (`over`) and the `unreadable` /
`incomplete` FACTORY_DEFECT cards still fire for a config with hand values. M5: none recorded. That is acceptable as a
named residual if j2 follows directly. Say so in E13 as "a path that asks remains for hand-written configs until j2".

## Not established

- The exact byte margins of the four role ratchets and of `S5_PLAN_BRIEF_BYTES_MAX` against a brief with the new line. I did
  not run the slow brief tests; the Lead's "1-8 B, plan brief at ceiling" is taken as the given input, and F3 holds for any
  margin under 37 B.
- Whether the `QA-9` seed of `role_brief_ratchet` selects a stand. That decides whether F3 (i) alone pays the cost.
- How many scaffold-based tests besides `landing_limit` assume the 100 s limit.
- Whether a signed-out landing on the cmp2 stand would have been slow (no run): the K7 judgment that route (a) is a floor
  is reasoned from `wait_until="load"` and Vite's on-demand serving, not measured.
- Whether `test_judgment_census.py` counts `check_stand_page_load` (notes only) as a unit. The card says no unit. The test
  is slow, so this is left to the canon.
- D13 movement in j2: the card's own stop rule covers it.

## Trail

Read: card r2 whole; r1 card (given, by the r2 references); `gate_preflight.py` :150-210, :2780-2830, :3089-3118,
:3275-3345, :6080-6095; `manual_capture.py` :95-115, :225-232, :550-575, :1630-1720, :1801-1818, :2255-2265, :2990-3060,
:3172-3182, :3405-3416, :5376-5388; `env_probe.py` :449-488; `stand_identity.py` :149-155; `investigation_probe.py`
:412-424; `walk_session.py` :1216-1222; `driver_gates.py` :118-122; `skills/qa-story/phases/s4.md` :17-20;
`references/config-keys.json` :720-735; `references/manual-evidence.md` :50-60; `test_manual_capture.py` :1650-1674;
`test_brief_pack.py` :2400-2441; `test_brief_pack_s5_plan.py` :38, :73, :542-600; `test_gate_preflight.py` :3651-3655,
:3804-3811; k-cards r2 :21-60, :568-590, :707-730; `tools/critic_verdict.schema.json`.

Searches (all case-insensitive, Grep tool):
- `page_object_max_wait_s|e2e_page_load_s` over the package. Positive control: the gate_preflight hits.
- `stand limit|stand_limit|page load|_e2e_limit|e2e_stand_limit|timeout_for|skip_stand_limits` over the package, with
  test_gate_preflight excluded.
- `limit_seconds|measurement_is_stale|E2E_LEVEL` over the package.
- The deleted names over package `*.md`, `docs/` and `tools/`. No hit in `SIBLING_MAP` or factory-map; the positive
  control is the `factory-rules-debt.md:111` hit.
- `needed_by` over `scripts/`.
- `brief_pack.py|manual_capture.py|judgment-census.json|...` over the three sibling r2 cards.
- `LANDING_LIMIT` over the tests.

Reruns: none. This was a plan review; no test sets were run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: timeout_for signature change breaks investigation_probe.py:419 and walk_session.py:1221, outside j1 owns; card also misses manual_capture.py:3015, :3178, :5383",
    "F2: timeout_for = signed-out load + 30 shortens the 180 s limit for sign_in landing (manual_capture.py:3015/3021) and the gate probe (gate_preflight.py:2808), which leads to not_landed and a PERSON_DECIDES card (gate_preflight.py:2788-2792): a person is asked; fix with max(180, load+30)",
    "F3: STAND_LOAD_ROLES hits the S5 plan critic brief (test_brief_pack_s5_plan.py:542, at ceiling, not in owns) and four ROLE_BRIEF_BYTES_MAX rows; no payment named",
    "F4: fixtures/manual-evidence/scaffold.py:68 writes e2e_page_load_s 70; test_manual_capture.py landing_limit (LANDING_LIMIT=100, :1467, :1657-1674) goes red under j1; not named"
  ],
  "fixes": [
    "F1: add investigation_probe.py and walk_session.py call lines to j1 owns (or keep a compatible signature)",
    "F2: max(DEFAULT_TIMEOUT_S, load_s+margin); flip rows; edit references/manual-evidence.md:57; brief line says floor, not fit-to",
    "F3: no line without a selected stand or a due measurement; exclude s5_plan dispatches; name AR-20 raises per role",
    "F4: name landing_limit and LANDING_LIMIT; seed a stand_load record or move to 180; scaffold.py measured block in owns",
    "F5: read returns none when the row's address differs from frontend_of url",
    "F6: config-keys.json needed_by in j2 owns (remove two) and j1 owns (add stand_load readers)",
    "F7: split failed by owner; stand-side failures not reused, not called a factory defect",
    "F8: concurrent-writer edge named or locked; rewrite section E against k-cards r2 queues (C3-k3 manual_capture.py, C3-k4 census :826)",
    "F9-F11: resolve goto, definition_sha_for(name), frontend_of url, _safe_url; skip_stand_limits meaning in changelog; name the j1-j2 window residual in E13"
  ],
  "class_completeness": "Class: readers of the deleted or redefined stand-limit fields. Checked with a case-insensitive package grep, positive control included. Missed siblings: 5 timeout_for callers (F1), scaffold fixture (F4), config-keys needed_by (F6), manual-evidence.md:57 text (F2). SIBLING_MAP and factory-map: no hits. Brief-ratchet axis missed (F3).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/manual_capture.py",
      "ai-packages/qa-factory/scripts/env_probe.py",
      "ai-packages/qa-factory/scripts/stand_identity.py",
      "ai-packages/qa-factory/scripts/investigation_probe.py",
      "ai-packages/qa-factory/scripts/walk_session.py",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/skills/qa-story/phases/s4.md",
      "ai-packages/qa-factory/references/config-keys.json",
      "ai-packages/qa-factory/references/manual-evidence.md",
      "ai-packages/qa-factory/scripts/tests/test_manual_capture.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py",
      "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py",
      "docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": []
  }
}
```
