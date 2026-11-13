# Critic on plan — "told before the work" mechanism spec (13.11.2026)

Under review: `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` (designer draft, T0–T10, forks F1–F11).
Against: Lead plan `20261113-plan-fabrika-ne-huzhe-agenta.md` §12, §13, §15; owner's word 13.11.2026 (one mechanism, not
patches, later fixes cannot breed the problem again). Package facts read ONLY from the origin/main worktree
`.claude/worktrees/read-main` at `fb36ae5` (written `pkg:` below). Review of a plan: no code exists, no tests to re-run; the
mechanical layer here is fact checks by Grep/Read/awk with positive controls (listed in the trail).

Verdict in short: the core shape (rows keyed by check id, one constructor on top of N0, a shrink-only bare/tagged ratchet,
the A24 join by computed key, F1-B/F2-a/F5/F6/F9) is sound and buildable. Six findings block: the spec builds a second
"what code checks of you" carrier beside two that already exist (the generated key page of `contract_slices.py` and
`design/role-rules.json`); F3-a changes refusal TEXT that crosses a process boundary, which breaks the accepted N0 invariant
and E9's claim and can re-route the driver's known-refusals table; the controller DOES reach a role (so 0.4, T9, F4, F10 and
owner question Q1 stand on a false fact); the scanner's closed list of list names misses refusal lists, the wrong error
direction for a gate; the check id is lost through the role-CLI transport `run_guarded`; T1's schema migration misses a
second reader of `stage-joints.json`.

---

## K1 — facts by trail

| # | Spec claim | Carrier on read-main | Verdict |
|---|---|---|---|
| 0.1 | A24 102 entries, 25 `kind: operation` | Grep `^    \{"id": "` → 102, `"kind": "operation"` → 25 over `pkg:scripts/refusal_registry.py` | fit |
| 0.2 | `role_cli.refuse` + `role-commands.json` is a second "one source, two readers"; 31 rows; read only via `--help` outside tests | `pkg:scripts/role_cli.py:1-20` (docstring), `:64-71` `epilog`, `:74-86` `refuse`; 31 commands (json load); case-insensitive Grep `role-commands\|role_cli\.(epilog\|shape\|entry\|registry)` outside tests → only `brief_pack.py:149` (comment), `reference_snapshot.py:174`, `red_sandbox.py:2231`, plus docs/CHANGELOG/`architecture.md:108`/`role-rules.json:255` | fit. But the spec misses what `role_cli.run_guarded` does (`:163-164`): every `ValueError` raised inside a role CLI becomes `refuse(command, str(exc))` — see B5. `refuse` signature today is `(command, problem, stream=None)`; T2's `refuse(command, problem, check=None)` drops `stream` (used by tests) — a T2 note |
| 0.3 | census 951 rows; per-role ratchet qa-automator 169 … conductor 476 | `pkg:scripts/tests/fixtures/judgment-census.json`: `grep -c '^  {"file": '` → **1142**; ratchet `:4` `blocking_per_role`: qa-automator **173**, qa-test-strategist **171**, qa-case-critic **164**, qa-requirements-tester **157**, others 139–140, conductor **680** | **defect (stale)**: the OH8-7b..7h chain (merge `d49c334`, wave 19) widened the census. Numbers are not load-bearing for the design, but the blind-spot list of §2.3 is (see B4/K3): "a subclass of ValueError raised by name (named blind spot already)" is now SEEN (census header `:3`, `test_judgment_census.py:22-24, 36-45`) |
| 0.3b | census `roles` is a coarse label, over-inclusion is "the safe direction" | `roles` is a HAND label checked only for form (`test_judgment_census.py:338-344`); a known under-label exists: `controller.py::_s3_completion_gate` is `["conductor"]` yet reaches the strategist (B3) | **defect**: the "safe direction" claim is false at least once |
| 0.4 | controller rows carry no `qa-` role → controller is conductor-only | `grep -cE '"file": "controller.py".*"roles": \[[^]]*qa-'` → 0 (positive control same shape on guard_pre_tool.py → 22): the LABEL fact holds. The behavioural conclusion does not: `controller.py:7513` raises `StateConflict("S3 structured test plan invalid: …")`, the driver routes it by `STRUCTURED_RE` (`driver_dispatch.py:36, 89`) to `resume_structured`, which resumes the ROLE's own session (`driver_machine.py:515-539`, comment: "the role's own session gets the refusal, ONCE per dispatch… Never the conductor") | **defect — B3** |
| 0.5 | the card is never trimmed; `BRIEF_MAX_BYTES = 6*1024`; pin `CARD_MAX_BYTES = 1200`; ahead-cards note | `pkg:scripts/brief_pack.py:54`; card rendered `:4424-4426`; last-resort comment `:4483` "the card is the one thing that cannot go"; ladder `:4454-4514`; `test_ahead_cards.py:52, 249`; `ahead-cards.json:3` | fit on substance (line cites drifted ~+30). But see N3: the card is not trimmed, yet a growing card evicts OTHER sections and prints an over-budget line to the role (`:4527`) |
| 0.6 | N0 not landed | Grep `check_id\|with_check\|checks\b` over `detector_verdict.py`, `driver_core.py` → no definition (3 prose hits of the word "checks"); positive control `^def \|^class ` → `class Record(str)` `detector_verdict.py:90` | fit |
| 0.7 | `sites()` is the one scanner, takes `files=` | `architecture.md:142` (AR-29 carriers) fit; but `sites` is now `refusal_registry.py:1187` with a THIRD keyword `raises=` fed by `raise_family()` (`:1127`), used by the census (`test_judgment_census.py:223-224`) | **defect (stale, design-relevant)**: T0's new `transports=` keyword would be a second widening switch beside `raises=` — fold into one (N5) |
| 0.8 | `expected_of_the_receiver` is what a handoff asks of the next role | `architecture.md` AR-10 carriers list it; spec reading accepted | fit |
| §4 | shape counts | `deny(\|block(`: guard_pre_tool 30, stage_guard 24, host_adapter 9, hooklib 1 — match; inject_context **8** (spec 1) | minor drift; T0 recounts, not load-bearing |
| AR-10 | spec's AR-10 row names `stage_joints` as the carrier set | `architecture.md` AR-10 Carriers: `handoffs/*.yaml`, `handoff_init.py`, `handoff_check.py`, **`scripts/contract_slices.py`**, `guard_pre_tool.py`; Detector: **`test_field_producers.py`**, A9, **`selftest.py --slices`**, `test_stage_joints.py` | **defect — B1**: two of AR-10's own carriers never appear in the spec |

Negative claims I rely on, each with a same-shape positive control (case-insensitive Grep on the spec file):
`contract_slices|handoff-keys|key page|inject-map` → only `inject-map` (F10 line, NOT-read list), so `contract_slices`/`handoff-keys` are absent; `role.rules` → 0, control `role.commands` → 10; `field_producers` → 0, control `stage_joints` → 19.

## K2 — one mechanism (AR-13/14/15)

Carriers of "what code will check of a role" that remain after T10:

| Carrier | Spec's treatment | Verdict |
|---|---|---|
| `contract_slices.py` key page `references/slices/<role>/handoff-keys.md` — GENERATED per role from `artifact-writers.json`, `validate_artifacts.PHASE_JSON_KEYS`, `stages.json` (required outputs, detectors), `stage-joints.json` (producers whose `told` path is the page: their `demands`) and the handoff form (`contract_slices.py:436-502`); injected via `inject-map.json` (`:22, 30, 38…`); stale page refused by `--check`/`selftest --slices`. 14 of the 50 `told` legs of today's `stage-joints.json` point at it | **silently left** — never named. The new brief section `## What code will check of you` with `requirement_from: validate_artifacts.PHASE_JSON_KEYS` and `handoff_form` re-renders exactly what this page already renders. Two generated roads to one fact = P31/AR-15 breach. **B1** |
| `design/role-rules.json` (451 rows, "mandatory rules of role texts", one reader `role_rules.py`, anchors in `agents/`, `skills/`, `references/`, `handoffs/`; e.g. `blocked-row-names-every-instance` `:7`, a rule `s5_precheck` judges) | **silently left** — never named. T7 "moves hand sentences into rows" and axis-31 line "agents keep pointers" without saying what happens to the role-rules row whose anchor is that sentence (the reader goes red when the sentence leaves the carrier, `role_rules.py:4-8`). A check's requirement then lives as a role-rules sentence AND a stage-joints sentence. **B1** |
| `ahead-cards.json` | absorbed card by card, `hand_cards` 12 → 0 (F7) | fit |
| `role-commands.json` / `role_cli` | joined as `requirement_from` (F6) | fit, with B5 |
| `window_record.REQUIRED_ROW_FIELDS` | joined as `requirement_from` | fit (axis 23/28 respected) |
| handoff forms / `handoff_init.py` skeleton | `requirement_from: handoff_form` | fit as a join, but duplicated by the key page (B1) |
| phase skills `skills/qa-story/phases/*.md`, `agents/*.md` prose | not counted; axis 31 pointer line | question: hand prose that states a check's requirement is a told carrier the walker cannot see; the spec should say these are NOT told legs for K2 (only the card/key page are), so prose never satisfies K2 |
| `expected_of_the_receiver` | neighbour, no change | fit |
| A24 REGISTRY | joined by `check_of` (F1-B) | fit |

AR-13: `contract_slices._keys_outputs` reads `stage-joints.json` directly (`contract_slices.py:490`, `_json_of`), not through `stage_joints` — the spec's "one reader of the rows (`stage_joints.row_for`)" is false today and T1 does not fix it (B6). AR-14: `refusal()` writing `Record(check=…)` directly makes it a second writer of `check` beside N0's `with_check`/`detector_records`; have `refusal` call `with_check` (N6).

## K3 — cannot be bred again

- On the execution path: yes. `selftest.py --contracts` runs `test_stage_joints.py` (`selftest.py:558`), CI `forge-check.yml:172` (read-main). fit.
- Where the role filter lives: K4's "role-reachable" and E3's `conductor_only` need the census, which is test-only (FR-44, `test_judgment_census.py:5`). `stage_joints.py` (a package script) may not read it. K4's role-filtered parts and the `conductor_only` count must run in `test_stage_joints.py`, not in `stage_joints.audit`/its count line (N1).
- Can a builder add a role-facing refusal the scanner does not see? Yes, by at least these roads:
  1. Name the error list outside the closed set `errors, problems, gaps, findings, out`. Measured over `pkg:scripts/*.py`: `reasons.append(` 87, `failures` 27, `bad` 27, `missing` 12, `finding` 18. Real refusals among them: `acceptance.py:160-182` (`reasons`, census roles include `qa-case-critic`), `case_forms.py:70-103` (`reasons`, case-id form refusals). The scan claims "never err toward MISSING" (§2.3) and then uses a hand list of names, which is the wrong direction. **B4**.
  2. The census's own still-unseen raise shapes (`raise _factory(...)`, `raise self._method(...)`, alias `E = MyErr; raise E(...)`; 52 functions measured, census header `:3`) — §2.3 lists an outdated blind-spot set and does not inherit the census's. **B4**.
  3. `sys.exit("message")` / `raise SystemExit("message")` (string argument: printed to stderr, exit 1) and a stdout JSON hook decision written without `hooklib.block`. Neither is in WIDE_TRANSPORTS. (Grep for `sys.exit("…")` today → 0, so this is a breeding road, not a backlog.)
  4. Swapping inside a file: convert one bare site to `sourced` and add a new bare one — the per-file count stays equal. Inherent to count ratchets; acceptable if named (N7).
- The structural backstop the spec does not use: the census already finds check UNITS by name (`UNIT_NAME_RE`), by refusal site, and by `BLOCKING_ENTRY_FILES` (`test_judgment_census.py:69, 78-79`), and C1 demands a row for each. A test-side direction "every blocking census unit with a non-conductor role contains a `sourced` site or is counted in a per-file `untold` ratchet" catches shapes the transport scan cannot see, because unit detection does not depend on the transport. The `untold` counter is named in §1.1/T1(f) and never defined. Defining it this way is the smallest fix that makes "cannot be bred" hold beyond the scanned shapes (part of B4's fix).
- Universe from code, not hand-listed: site detection, yes (AST). Role reach, no: census `roles` is a hand label (above), so the gate is only as good as the label, and B3 shows a known wrong label. Under-labelling is caught by C11/G1 at run time only — an honest gap that must be named as such, not as "the safe direction".

## K4 — architecture and principles

| Item | Verdict | Evidence / note |
|---|---|---|
| AR-9 | fit, question | the door rides from the row. "Red when the row's roles have no such door in their tool set — presence only": if that means reading the door SENTENCE for a tool name, it is a phrase reading (FR-12). Make it data only: `when` token × `host_adapter.role_has_bash` (`host_adapter.py:519`), never the door text (N8) |
| AR-10 | defect | carriers `contract_slices.py`, `test_field_producers.py`, `--slices` ignored (B1) |
| AR-13 | defect | second reader `contract_slices.py:490` (B6); otherwise fit (`null_outcomes.load_data` is today's reader, `stage_joints.py:604, 646, 668`) |
| AR-14 | fit after N6 | |
| AR-15 | defect | survivor choice ignores the existing generated page and role-rules (B1) |
| AR-18 | defect | `spoken` is "the one renderer", yet `detector_verdict.render/joined/compound` and `'; '.join(errors)` sites stringify a Record to the problem only (`render` does `str(line)`, `detector_verdict.py:446`); `sourced` at the site does not mean expected/door reach the role (B5) |
| AR-20 | fit | new counters shrink-only, raises named |
| AR-22/23 | fit | zero-row line (E8) |
| AR-28 / FR-59 | fit | I-P: a missing row never passes or crashes |
| AR-29 / P27 | fit | K1–K5 are presence/xref/shape; J1/J2 sentence truth goes to the critic → Lead. No code check judges a requirement sentence |
| FR-1, FR-2, FR-38 | fit in intent | |
| FR-12 | question N8 | |
| FR-13 | fit | `when_kinds`, `requirement_from` closed lists are data |
| FR-44 | defect N1 | census is test-only; the role filter cannot live in `stage_joints.py` |
| FR-45 | fit | the walker stays pure |
| FR-47 / P1 | fit | |
| P2 | fit | |
| P15 / P22 | defect via B3 | the conductor exclusion rests on a false premise |
| P31 / axis 34 | **defect** | two roads for "what code checks of you" (brief card + key page), B1; the conductor/controller exclusion has no data row and its owner question rests on a false fact (B3) — rule 19 blocks both |
| Owner's "no ceiling in a run" | defect N3 | E12 "no truncation anywhere in the package" is false: `detector_verdict.FINDINGS_MAX_BYTES = 6000` (`detector_verdict.py:63`) moves findings past 6 KB to a side file (`render` `:439-453`), and `BRIEF_MAX_BYTES` (`brief_pack.py:54`) still drives the trim ladder and prints an over-budget line to the role (`:4527`). Appending expected/door to every finding roughly doubles each line, so fewer findings show inline: the cmp3 regression C2-1 that `detector_verdict.py:4-6` records. Name the dependency on whichever node removes the in-run ceiling (the amendment's B1 rules) |

## K5 — edges

| Edge | Verdict | Note |
|---|---|---|
| E1 | fit | |
| E2 | defect (N2) | census labels guard units with all 12 roles (spec 0.3), so K5 (census roles ⊆ row roles) is satisfied by `*`. K2 judged per role then demands a told leg for every no-shell role on a `when: shell` row, which the card deliberately omits. State that K2 per role intersects with the `when` eligibility. "Lead fixes the census label" also needs T4 to own the census fixture, which it does not |
| E3 | defect (B3) | |
| E4, E7, E8, E11, E13 | fit | |
| E5 | defect (B3) | "under-labelling is caught by a run" — a known instance exists today and needs no run |
| E6 temporal | defect (B6) | "the reader reads only v2 after T1" names only `stage_joints`; `contract_slices._keys_outputs` (`:490-501`, reads `joints[].producers[].roles/told/demands`) and `retro_numbers` (`threshold`, `retro_numbers.py:1236`) also read the file. The second is unaffected only if `friction` stays at the top level, which v2 keeps. Both worlds otherwise decided correctly |
| E9 person's word | **defect — B2** | the claim "split_overridden and finding_key see the Record's str value" holds in-process only. Form 1 crosses a process boundary: a detector prints `- [<check> <id>] <problem> — fix: <repair>` and `detector_verdict.parse` rebuilds Records from the PRINTED line (contract `detector_verdict.py:9-23`), so §2.3's form-1 rule (door as ` — fix: <door>`, expected appended when there is no fix part) CHANGES the text that `waiver.split_overridden` matches with `contract.names_whole` over the whole line (`waiver.py:215-217`). A recorded word whose identifier appears in a filled door or requirement (an instance id from `<ID>`, a field name) passes a line it did not pass before. That is the opposite of E9's invariant, and the T2 row tests only the in-process path |
| E9b (not named) | **defect — B2** | the driver routes refusals by regex over the WHOLE printed text, first match wins (`driver_machine.match_known` `:47-64`, `KNOWN_REFUSALS` `driver_dispatch.py:38-89`; its own comments warn that embedded words like "expected_revision", "stands in front of gate" or "STORY BUDGET" let an earlier row win, `:43-59`). Appended expected/door sentences can re-route a refusal (to `ask_person`, `continue`, `recover`), and a sentence carrying `role_cli.PERSON_MARKER`/`REPAIR_MARKER` overrides the table outright (`:57-60`) |
| E10 | fit with a note | also `structured_resumes`/one-resume keys are `finding_key` of the lines (`driver_machine.py:529-533`): text change → one extra resume per in-flight dispatch. Accepted cost; name it |
| E12 | defect (N3) | above |
| P1-v N0 invariant | **defect — B2** | N0 (`p1v:162-163`): "the text of every record is byte-identical to today's (finding keys, split_overridden, the person's words see the same strings)". F3-a contradicts it for every form-1 producer that T5/T7 migrate |

## K6 — feasibility

- T0 gate thresholds: "≥95 % classified without walk error" is undefined before T2. No constructor exists, so every site is trivially `bare`/`tagged`, and `sites()` has no "walk error" today. Define it (a site whose transport argument the AST cannot resolve, or a file that fails to parse) or drop it. "Census join ≥90 %" needs a join that the named command (`refusal_registry.py --sites --wide --json`) does not do, and C5 forbids a forge-side script, so the join is unreproducible as written. Name where it runs (a T0 row in `test_refusal_registry.py`, or a `--census <path>` input to the flag used only by the test). M3 (Lead classifies 30 samples, precision ≥80 %) is measurable. (N4)
- The census join as a role-reach source: sound for SITE→UNIT (C1 demands a row for every unit the scanner sees), unsound as ground truth for UNIT→ROLES (hand label, B3 instance).
- Migration size: honest in order of magnitude (834 `errors.append(` alone across the package). Too coarse in cut: T7a `validate_artifacts.py` (250 append sites in the spec's count) is one node, and each family needs a requirement sentence that J1 judges. That is designer-grade writing for a weaker model; cut T7a by function as T7e already does (N9).
- T1 baseline: meaningful for the scanned shapes only; with B4's fixes (no name filter, plus a census-unit `untold` direction) it becomes meaningful for the class.
- Runtime: `detector_verdict.refusal` → `stage_joints.row_for` puts the walker module (whose heavy imports include `stage_guard`, `inject_context`, `stage_joints.py:24-26`) on the path of every hook refusal (`hooklib.block` → `detector_verdict` → `stage_joints` → … → `hooklib`). Keep `row_for` in a small reader with no walker imports (N10).

## K7 — nodes for a weaker model

- T0, T1, T2, T3: file, function, behaviour, test rows named; direction chosen. fit (subject to B-fixes).
- T4: owns name only `rule_typed_runner`, `check_command` in `stage_guard.py`, but `deny/block` also sit in `check_dispatch` (9), `_check_exploration` (5), `check_resume` (3), `check` (2) (awk over `stage_guard.py`). `inject_context.py` (8 hits) is owned by no node, although §5's completeness line sends its role-reachable sites "to T4". Orphaned sites; T4 also needs the census fixture if E2's relabelling is its job (N2, N11).
- T5–T7: "the `*_problems` builders", "refusal sites incl. …" are not function lists. PROJECT.md «Командная работа» item 3 asks for function lists on hot files; manifest_put/run_suite need them (N11).
- Shared files: `stage-joints.json` rows queued T1 → T3 → T4 → T5 → T6 → T7, while T4/T5/T6 are marked "parallel". Code can run in parallel; rows merge in queue order. Say so explicitly. `test_stage_joints.py` T1 → T3 queued: fit. `brief_pack.py` after P1-v N3: fit.
- Tests: keep-file rows and tables, no new file. Conforms to `docs/TESTING.md:55, 96, 117`. The `CARD_MAX_BYTES` pin kept "for hand text" is the forbidden kind "Пин измеренной константы… потолки brief_pack" (`TESTING.md:95`). F8 should remove it outright, not keep it for hand text (N12).

## K8 — crossings

| Work | Verdict |
|---|---|
| P1-v N0 | one producer of `check`: fit (F5); contradiction on text invariant: B2; AR-14 second writer: N6. N0's fallback ids `<stem>:unlabelled`/`unknown` (`p1v:149-150`): K1 must say they never need rows and how C11/G1 count them (N13) |
| P1-v R-8 | P1-v itself records that controller structured refusals resume the ROLE with `["unknown"]` (`p1v:142`). This spec's T9 contradicts the accepted neighbour (B3) |
| P1-b C11 | fit as a call (F9); with B5 unfixed, C11 verifies the `role_cli:<command>` row instead of the check that actually refused |
| FV1-18 / FV1-19 / FV1-27 / FV1-30 | consistent with plan §12 and §15 (FV1-30 direction chosen by the amendment's F-A3-5); finding files not re-read (not in the manifest) |
| `field_cards.py` proposal | "absorbed" is right in intent, but the existing generated key page is the closer survivor (B1) |
| `ahead-cards.json` | fit |

## K9 — the Lead's fork decisions (plan §15)

| Fork | Verdict | Consequence missed |
|---|---|---|
| F1-B | fit | — |
| F2-a | fit | the rename of 43 keys also touches pins in `test_stage_joints.py`/`test_stage_joints_12586.py` and P1-b C1; list them in T1 |
| F3-a | **consequence missed** | the text crosses processes: N0 invariant, E9, KNOWN_REFUSALS routing, FINDINGS_MAX_BYTES (B2, N3). Smallest correction: F3-a for in-process transports to the role (hooks' `block`/`deny`, `role_cli.refuse`), and form-1 finding lines byte-identical (the card already told the requirement; `expected`/`door` at most in the tail, which `parse` does not read as a finding) |
| F4 out | **not fit as decided** | rests on 0.4, contradicted by `resume_structured` (B3); Q1 to the owner states a false fact ("роли их не получают") |
| F5 | fit | — |
| F6 join | fit | `run_guarded` collapses inner refusals into `role_cli:<command>` (B5) |
| F7 | fit | `hand_cards` should also count role-rules sentences that are check requirements, or B1's join decides it |
| F8 | partly | keep-for-hand-text conflicts with TESTING.md (N12); the card's growth still drives the 6 KB ladder (N3) |
| F9 | fit | — |
| F10 census | **consequence missed** | hand label with a known under-label (B3); test-only, so the gate's role split must live in the test (N1) |
| F11 | fit | — |
| "by price" order (Q2) | fit | — |

## Duplication and consistency (rule 18)

Found: the new brief card duplicates the generated key page (`contract_slices.py:436-502`) for PHASE_JSON_KEYS, handoff-form fields and joint demands (B1). Requirement sentences would live both in `role-rules.json` and in `stage-joints.json` (B1). A second widening keyword `transports=` beside `raises=` (N5). Grepped: `contract_slices|handoff-keys|role.rules|field_producers` in the spec (absent, controls above); `stage-joints.json|stage_joints` readers in the package (26 files, readers `contract_slices.py`, `retro_numbers.py`, `null_outcomes.py`).

## Code quality (rule 18)

No code under review. Design quality: the constructor/`spoken`/row split is clean. Two smells: `Record.__str__` = problem while the transports must remember to call `spoken` (B5: the default silently drops the told part), and the walker module on the hook runtime path (N10).

## One action, one road (rule 19, P31)

Blocks: (1) two roads telling a role "what code checks" — brief card and key page (B1); (2) the conductor/controller exclusion has no data row and no owner's word yet, and its premise is false (B3). Fix in this round; no residual to pass on.

---

## Blocking findings

**B1 — the survivor ignores two existing AR-10 carriers (key page, role-rules).** Where: §0, §1.1 AR-10/AR-15 rows, §2.5, T3, T6, T7, F7. Why it blocks: the owner asked for ONE mechanism. `contract_slices.py` already generates a per-role "what the gate reads of you" page from carriers, including `stage-joints.json` (`contract_slices.py:436-502`; AR-10 carriers in `architecture.md`; 14 told legs point at it). `design/role-rules.json` (451 rows) already registers role rule sentences with anchors. The spec adds a third carrier and never names the other two, so after T10 one requirement can be told in three places that drift. Smallest fix: a §0 fact row for each; one decision (a Lead fork): either the brief card IS the key page's renderer (`requirement_card_lines` called by `contract_slices._keys_outputs`, or the key page retired into the card, its `--slices` check moved), or the card is rendered into the key page and the brief keeps a pointer. And: a row whose requirement has a role-rules row names it (`role_rule: <id>`), or T7 retires the role-rules row in the same diff ("role-rules: retire <id> -- <word>", `role_rules.py:7-8`). Re-pass of the critic on this decision (it changes architecture, PROJECT.md step 6).

**B2 — F3-a changes cross-process refusal text: breaks N0's invariant, E9 and the driver's routing.** Where: §2.3 (form-1 rule), E9, E10, T2(e), F3. Why: form-1 lines are reparsed from printed text (`detector_verdict.py:9-23`), and `split_overridden` matches identifiers over the whole line (`waiver.py:215-217`), so a door/requirement appended to the line changes which lines a recorded word passes. `match_known` routes on the whole text with first-match-wins and marker override (`driver_machine.py:47-64`, `driver_dispatch.py:38-89`). P1-v N0 requires byte-identical record text (`p1v:162-163`). Smallest fix: form-1 finding lines stay byte-identical (no door/expected in the finding line). Expected/door print only from in-process transports (`block`, `deny`, `role_cli.refuse`) AFTER the problem, in lines that the driver's match does not read: either match on the problem part only, or add a T2 row asserting `match_known(spoken(r)) == match_known(str(r))` for every row's filled text. E9's T2 row runs through `detector_verdict.parse` on printed text, not an in-process Record.

**B3 — the controller reaches a role; 0.4, E3/E5, T9, F4, F10 and Q1 stand on a false fact.** Where: §0.4, §3 E3/E5, T9, §9 F4/F10, §10 Q1. Why: `controller.py:7513` (`_s3_completion_gate`, census `["conductor"]`) → `STRUCTURED_RE` → `resume_structured` → the strategist's own session (`driver_machine.py:515-539`); P1-v already records this road (`p1v:142`). The owner would be asked to approve an exclusion on a wrong premise. Smallest fix: correct 0.4 and Q1's text. Put the role-resumed controller refusals (at least everything matching `STRUCTURED_RE`) in the universe with rows (their requirement is planning_contract's, T7b). Fix the census label of `_s3_completion_gate` (and any other unit on a `RESUMABLE_HEADS`/`STRUCTURED_RE` road) to include the role. Rephrase F10's "safe direction" as "hand label; known under-labels fixed here; the rest caught at run time".

**B4 — the gate's scan errs toward MISSING: closed list names and stale blind spots.** Where: §2.3 error direction, §2.4 WIDE_TRANSPORTS, T0(b,d). Why: refusal lists under other names exist today (`acceptance.py:160-182`, `case_forms.py:70-103`, `reasons`), and a builder can breed a new one by naming a list `reasons`. §2.3's blind-spot list predates OH8-7h and misses the census's 52 factory/method-raise functions. Smallest fix: drop the name filter (any `.append/.extend/+= [str]` inside a census-blocking unit counts; over-count is the declared safe side); inherit the census header's blind-spot list verbatim; add `sys.exit(<str>)`/`SystemExit(<str>)` to WIDE_TRANSPORTS. Define `untold` as the census-unit direction (every blocking unit with a non-conductor role has a `sourced` site or counts in a per-file shrink-only `untold`), test-side.

**B5 — the check id and the told part do not survive stringifying transports.** Where: §2.3 transports list, T2 owns. Why: `role_cli.run_guarded` turns `ValueError(refusal(...))` into `refuse(command, str(exc))` (`role_cli.py:163-164`). `str(Record)` is the problem, so the id becomes `role_cli:<command>` and the specific row's expected/door are lost. P1-v G1 and P1-b C11 then attribute the refusal to the wrong check. The same holds for `detector_verdict.render/joined/compound` (`:446`) and any `'; '.join(errors)`. A site counted `sourced` can still reach the role bare. Smallest fix: T2 owns `run_guarded` (if `exc.args[0]` is a Record, pass its check through) and lists every stringifying transport the scanner treats as a sink. A T2 table row per transport asserts a Record passed through keeps `check`; `sourced` is counted only when the site's sink is in that list.

**B6 — T1's schema migration misses a second reader of `stage-joints.json`.** Where: E6, T1 owns, AR-13 row. Why: `contract_slices._keys_outputs` reads `joints[].producers[].roles/told/demands` directly (`contract_slices.py:490-501`). A v2 change to producers, or the rename, can silently empty the "The gate also reads" lines, and the generated page goes stale under `--slices`. Smallest fix: T1 owns `contract_slices._keys_outputs` (or B1's decision moves it). It reads rows through `stage_joints` (AR-13), and a T1 row asserts the generated key pages are unchanged by the migration.

## Non-blocking findings (fix in the same round; no residual lines)

- N1 — K4's role filter and `conductor_only` need the census (test-only, FR-44): place them in `test_stage_joints.py`; `stage_joints.audit` counts unfiltered per-file bare/tagged.
- N2 — E2/K2: told per role intersects with `when` eligibility; T4 owns the census fixture if it relabels guard units.
- N3 — E12 is false (`FINDINGS_MAX_BYTES` 6000, `BRIEF_MAX_BYTES` ladder, over-budget line to the role). Correct the text and name the dependency on the node that removes the in-run ceiling (amendment B1), and the inline-findings cost of longer lines.
- N4 — T0 gate: define "walk error"; say where the census join runs (test row or `--census` input).
- N5 — fold `transports=` into the existing `raises=`/`raise_family` widening of `sites()` (`refusal_registry.py:1127, 1187`).
- N6 — `refusal()` builds through `with_check` (one writer of `check`).
- N7 — name the per-file swap road of a count ratchet; consider per (file, function) counts.
- N8 — the door/tool-set check reads data only (`when` × `role_has_bash`), never the door sentence (FR-12).
- N9 — cut T7a by function; requirement sentences for its families drafted by the designer, not the builder.
- N10 — `row_for` in a small reader module without the walker's heavy imports (hook runtime path).
- N11 — T4: own `stage_guard` `check_dispatch`/`_check_exploration`/`check_resume`/`check` (or declare them code-only per census), and `inject_context.py`; T5 names functions of `manifest_put.py`/`run_suite.py`.
- N12 — F8: remove `CARD_MAX_BYTES` outright (TESTING.md:95 forbids ceiling pins).
- N13 — K1 says N0's `<stem>:unlabelled`/`unknown` ids need no row and are counted by C11/G1 as "no row".
- N14 — refresh stale facts: census 1142 rows and per-role ratchet, `sites` at `:1187` with `raises=`, brief_pack lines `:4344`, `:4426`, inject_context 8 hits, T2's `refuse` keeps `stream=`.

## Verdict

`fit after fixes` — 6 blocking findings (B1–B6), 14 non-blocking. B1 changes architecture, so per PROJECT.md "новая идея" step 6 its resolution gets a critic re-pass; B2–B6 the Lead can check against this file. The acceptance decision belongs to the Lead.

## Trail

Read (read-main `fb36ae5` unless noted): the spec whole; plan §12, §13, §15 (`:296-485`); P1-v spec `:120-194`, Grep of ceiling lines; `role_cli.py` whole; `refusal_registry.py` (Grep counts; `def` lines `:57, 1127, 1187, 1259`); `judgment-census.json` (`:1-6`, row counts, controller/guard role Greps, rows of `_s3_completion_gate`/`_decision_problems`); `test_judgment_census.py:1-100, 330-380` + Grep; `brief_pack.py:4415-4539` + Grep of constants; `test_ahead_cards.py` Grep; `ahead-cards.json:1-4`; `detector_verdict.py:1-119, 400-459` + `def` list; `driver_core.py` Grep (`:67-97`); `waiver.py:202-232`; `driver_machine.py:45-69, 510-539`; `driver_dispatch.py:30-69` + Grep `:89`; `controller.py` Grep `:3203, 7473, 7513` + function lookup; `stage_joints.py` `def` list, `:15-25`; `stage-joints.json` counts and `path` histogram; `contract_slices.py:436-515`; `role_rules.py:1-60`; `role-rules.json:1-12` + row count; `test_field_producers.py:1-25`; `host_adapter.py` Grep `:519, 567`; `inject-map.json` Grep; `architecture.md:106-125, 134-180`; `factory-rules.md` Grep FR-38; `forge-check.yml:165-176`; `selftest.py` Grep; `test-layers.json` keep/quarantine rows Grep; `docs/TESTING.md:36-125`; `docs/SIBLING_MAP.md` headings `:452-620`, axes 28, 31 text (root checkout: forge doc, not package).
Not read: FV1 finding files, the field_cards finding, P1-b spec, the amendment spec (`20261113-p1-specs-amendment-owner-words.md`), bodies of validate_artifacts/planning_contract/handoff_check/manifest_put/run_suite.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 survivor ignores two existing AR-10 carriers: the generated key page contract_slices.py:436-502 (references/slices/<role>/handoff-keys.md, 14 told legs point at it) and design/role-rules.json (451 rows); the new brief card is a third road (AR-15, P31)",
    "B2 F3-a changes cross-process refusal text: form-1 lines reparsed by detector_verdict.parse, split_overridden matches whole lines (waiver.py:215-217), match_known routes on whole text (driver_machine.py:47-64); contradicts P1-v N0 byte-identical invariant (p1v:162-163) and E9",
    "B3 controller reaches a role: controller.py:7513 (_s3_completion_gate, census conductor-only) is resumed to the strategist by resume_structured (driver_machine.py:515-539); 0.4, E3, E5, T9, F4, F10 and owner question Q1 rest on a false fact",
    "B4 the gate scan errs toward missing: closed list names miss real refusal lists (acceptance.py:160-182, case_forms.py:70-103 use reasons); blind-spot list predates OH8-7h (census header lists 52 factory/method-raise functions); sys.exit(str) not a transport",
    "B5 check id and told part lost through stringifying transports: role_cli.run_guarded refuse(command, str(exc)) (role_cli.py:163-164), detector_verdict.render str(line) (:446); sourced site can reach the role bare and C11/G1 attribute to role_cli:<command>",
    "B6 T1 migration misses second reader of stage-joints.json: contract_slices._keys_outputs reads producers roles/told/demands directly (contract_slices.py:490-501); AR-13 claim false; key pages can go stale"
  ],
  "class_completeness": "Class: a check's requirement reaches the role only at refusal. Map axes 17, 18, 23, 28, 32, 34 walked by the spec; missed carriers of the same class found outside its walk: contract_slices key page (AR-10 carrier), role-rules.json, run_guarded transport, controller resume_structured road, refusal lists named outside the closed set. Each is a blocking finding with its fix; no residual queued.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md",
      "docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:296-485",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md:120-194",
      "read-main pkg scripts/role_cli.py",
      "read-main pkg scripts/refusal_registry.py (counts, def lines)",
      "read-main pkg scripts/tests/fixtures/judgment-census.json:1-6 + rows",
      "read-main pkg scripts/tests/test_judgment_census.py:1-100,330-380",
      "read-main pkg scripts/brief_pack.py:4415-4539",
      "read-main pkg scripts/detector_verdict.py:1-119,400-459",
      "read-main pkg scripts/waiver.py:202-232",
      "read-main pkg scripts/driver_machine.py:45-69,510-539",
      "read-main pkg scripts/driver_dispatch.py:30-89",
      "read-main pkg scripts/controller.py:3203,7465,7513",
      "read-main pkg scripts/contract_slices.py:436-515",
      "read-main pkg scripts/role_rules.py:1-60",
      "read-main pkg design/role-rules.json:1-12",
      "read-main pkg design/architecture.md:106-180",
      "read-main pkg scripts/stage_joints.py def list,15-25",
      "read-main docs/TESTING.md:36-125",
      "docs/SIBLING_MAP.md axes 28,31 and headings"
    ],
    "reruns": [
      {"command": "Grep count ^    {\"id\": \" and \"kind\": \"operation\" in refusal_registry.py", "result": "102 and 25 (spec fact 0.1 holds)"},
      {"command": "grep -c '^  {\"file\": ' judgment-census.json", "result": "1142 (spec says 951: stale)"},
      {"command": "grep controller.py rows with qa- role; control guard_pre_tool.py", "result": "0; control 22"},
      {"command": "Grep check_id|with_check in detector_verdict.py, driver_core.py; control ^def|^class", "result": "no definition; control finds class Record(str) :90"},
      {"command": "grep -ohE '[a-z_]+.append(f?\"' scripts/*.py | uniq -c", "result": "errors 834, out 539, problems 323, reasons 87, failures 27, bad 27, missing 12"},
      {"command": "Grep -i contract_slices|handoff-keys|role.rules|field_producers in spec; controls inject-map, role.commands, stage_joints", "result": "absent; controls 1, 10, 19"},
      {"command": "awk deny/block call sites by function in stage_guard.py", "result": "check_dispatch 9, _check_exploration 5, check_resume 3, check 2, check_command 2"}
    ]
  },
  "fixes": [
    "B1: add facts for contract_slices key page and role-rules.json; Lead fork: card renders into the key page or replaces it; rows name role_rule ids or T7 retires them in the same diff; critic re-pass on this decision",
    "B2: keep form-1 finding lines byte-identical; print expected/door only from in-process transports after the problem; T2 row asserts match_known and split_overridden unchanged on printed text via parse",
    "B3: correct 0.4/E3/E5/T9/F4/F10/Q1; put role-resumed controller refusals (STRUCTURED_RE road) in the universe; fix census labels of those units",
    "B4: drop the list-name filter; inherit the census blind-spot list; add sys.exit(str)/SystemExit(str); define untold as the census-unit direction test-side",
    "B5: T2 owns run_guarded and passes a Record's check; list stringifying sinks; sourced counted only through Record-aware sinks; a row per sink",
    "B6: T1 owns contract_slices._keys_outputs, reads rows through stage_joints, row asserts key pages unchanged by migration",
    "N1-N14 as listed in the review file"
  ]
}
```
