# P1-b N4w: the exit-row walker (`--part exits:<group>`). DESIGNER DRAFT (t-805)

Status: designer draft (Opus), written from the Lead's intent brief of 14.11.2026 (t-805) plus the coordinator's extra input
(points (a) to (e) from the stopped builder of group s1-s4, answered in section 10). This draft edits neither the P1-b spec nor
the N0 round-3 amendment. Forks are in section 11 and none is closed here. Small choices I closed are in section 12, queue
lines in section 13, and the reading trail with negative-claim controls in section 14. Until the Lead accepts it, it is not a
dispatch. The card in section 5 can be run on the recommendations until the Lead decides (PROJECT.md «Командная работа» п. 11).

Trees and names: `BR` = `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n3` (branch `wip/p1b-n3` at 7ad7d20f); `T` = `BR\ai-packages\qa-factory\scripts\tests`.
"P1-b" = `BR\docs\tasks\specs\20261113-p1b-dry-story-spec.md`; "R3" = `BR\docs\tasks\specs\20261113-p1b-n0-round3-amendment-spec.md`;
"N2g" = `BR\docs\tasks\specs\reports\20261114-p1b-n2g-report.md`; "S0R" / "S14R" = the blocked builders' reports
(`...\p1b-n4-s0\docs\tasks\specs\reports\20261114-p1b-n4-s0-report.md`, `...\p1b-n4-s1s4\docs\tasks\specs\reports\20261114-p1b-n4-s1s4-report.md`).
Every line number below comes from reading these files on 14.11.2026.

Header of the node (R11-f):

given: this file (sections 2-9 and the Lead's decisions on section 11); P1-b §3.2-§3.6, §4.3, §4.4, §5 (E1-E22), §6 cards N3, N4, N4c, §9.3; R3 §5 (the `stub` grammar of a type row, E-R8); `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\` files `test_scenario_dry_1.py`, `dry_world.py`, `dry_exits.py`, `dry_stub.py`, `dry_driver.py`, `known_red.py`, `scenario_walk.py`, `harness.py`; fixtures `fixtures\driver-exits\*.json`, `fixtures\stories\dry-1\story.json`; `ai-packages\qa-factory\references\question-prices.json`, `stage-joints.json`, `conductor-actions.json`; N2g (the main pass as it runs today); S0R and S14R; `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (whole, PROJECT.md package change п. 1); `C:\QAFactory\forge-repo\plans\builder-rules.md`; `C:\QAFactory\forge-repo\docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\dry_driver.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\selftest\
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\ai-packages\qa-factory\changelog.d\p1b-n4w-exit-walker.md
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w\docs\tasks\specs\reports\20261114-p1b-n4w-report.md
(`dry_driver.py` is owned only under F-W4 (a). Functions per file: section 5.)
non-goals: real walk rows of any group (`fixtures\stories\dry-1\exits\*.json`, `seeds\*.json`, `fixtures\driver-exits\<group>.json`: the five N4 parts); `dry_stub.py` (the stub's control grammar is read as built, F-W1); `known_red.py` (the P1-a helper; imported only); `test_conductor_doors.py` (N4c); `scenario_walk.py`, `test-layers.json`, `selftest.py`, `slow_tests.json`, `canon.yml` (section 7 says why none changes); the checks C7, C8-as-expectation, C10 (section 4, F-W13); any driver, controller or gate code; P1-b's own text (amending §3.3 is the Lead's move after section 11)
handoff: builder report at the owns report path (rule 7 of `.claude/agents/builder.md`): the FR walk, the verbatim DoD runs, the seconds of every run, the walker's printed lines of the self-test group, the measured snapshot index (item 7), every deviation from this card named
edges: section 6 (EW1-EW26); P1-b E1, E6, E7, E9 (the `empty` variant only), E15, E16, E17, E18, E20
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` and `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:selftest --exits-root ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/selftest --ledger ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/selftest/known_red.json`; the full list with expected output is section 7
siblings: axes 5, 17, 18, 34 (section 9, with every axis enumerated); P1-b §7(b) for the axes this node leaves as P1-b left them
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-p1b-n4w-exit-walker-spec.md (this draft; the Lead names the accepted path)

---

## 0. Verdict in brief

- Most of the walker's PARTS already exist on `wip/p1b-n3`: snapshots and copies of them, the label check, the tree hash, one
  driver process per turn, the fingerprint (C3), the same-ask test and the loop judge (C5), the gate rehearsal (C6), the run-class
  check (E18), the label ledger reconcile, the walk-row loader and `driven_keys`. What is missing is the **executor of one exit row**
  (start, seed, answer, judgment, outcome line), the **`exits:<group>` part**, and a **group-level outcome and `unwalked` line**.
  Section 2 lists each part with file:line.
- Three facts of the built code shape the card more than the spec does:
  1. `main_pass` deletes its snapshots when it returns (`dry_world.py:1007-1008` -> `World.close` `:272-276`), so an exits part
     must make its own snapshots in its own process. The main pass took 381.2 s to its S5 stop (N2g `:43`). A part that re-runs it
     whole costs over six minutes before its first row (F-W5).
  2. A snapshot is taken at the END of a driver turn, not at the stage border (`dry_world.py:875-877`, after a turn of
     `--max-boundaries 60`, `:868`). So `S0` is the world waiting at the `s1_review` question, and `S1`..`S3` are the same world
     waiting at `gate_A` (N2g `:41`: "made S0, S1, S2, S3, S4" in 4 driver processes). A row aimed at an S2 state cannot start at
     `S2` (F-W6). The coordinator's point (d) agrees.
  3. The stub's control grammar as built (`dry_stub.py:632-655`, `:409-415`, `:91-115`; `story.json:7-80`) is NOT the `stub`
     grammar of P1-b §3.3 (`:257-259`). The walker cannot satisfy both (F-W1).
- §3.3 is silent or ambiguous on eight points the walker has to decide. They are forks (section 11), not inventions: the row-id
  namespace (coordinator point (a)), joint variants and `*` joints (point (b)), the variants of the keyless `conductor` kind (point (c)),
  how a route or joint firing is observed, what C2 means in practice, the expectation of the `empty` variant, the shape of
  `seeds/<group>.json` (named in N4's owns but given no grammar anywhere), and how a row is marked for owner questions Q1 and Q2.
- Recommendation: one sequential node N4w, before the five N4 parts. It writes the executor in `dry_world.py` (it collects data)
  and the judgment in `dry_exits.py` (pure functions, table-tested), and adds the part to `test_scenario_dry_1.py`. It is proved by
  a pure case table and by a small self-test group of real rows under `fixtures/stories/dry-1/selftest/`, which no census or
  `driven_keys` reads.

---

## 1. AR-n touched, the change checks, and the owner and class of each check

The node writes only under `scripts/tests/` (plus a changelog fragment and the report). Here "keeps" means the walker becomes a
detector of the invariant, or obeys it inside the test layer. The carriers of the invariants are not changed.

| AR | What the node does with it | Change check (in the DoD, section 7) |
|---|---|---|
| AR-28 (an unknown never becomes a pass) | Every row gets exactly one outcome. A row that is not run is a NOTE with its reason and is never PASS. An unreadable carrier is red naming the file. A part with no rows is red | pure-table rows EW1-EW8; e2e group line `outcomes` |
| AR-29 (code judges data) | The walker compares data only: the fingerprint, question records, the price-key record, the stub journal, `passed-by-person.jsonl`, the JSON field `gate_ready`. The outcome a row expects (verdict, conductor move, repair round) is SET by the row, never computed | grep of the new functions in `dry_exits.py` for `result_text`/`brief` reads: none (positive control: `result_text` is found at `dry_stub.py:849`) |
| AR-13 (a fact with a reader function is read only through it) | The fingerprint goes through `dry_exits.state_fingerprint`, the ledger through `known_red.load/reconcile`, prices through `dry_exits.scan_prices`, gate readiness through `dry_world.gate_ready`, the class through `dry_exits.class_of` | pure-table row: `judge_row` is called with facts and never opens a file itself (it takes a `facts` mapping; checked by the table feeding it synthetic facts) |
| AR-15 (one survivor per shared problem) | One road for the main pass and the prefix an exits part needs (`drive_main`, item 1), one loop judge (`loop_problem`), one reconcile (`known_red`), one output form (`scenario_walk.Result` -> `harness.check` / `NOTE`) | `--part main` prints the same line set as N2g `:33-44` (only timing figures differ; item 1, DoD 6) |
| AR-17 (one door to the conductor) | No attribute of `Driver` is assigned. The route recorder (F-W4 (a)) is a passing spy on the MODULE function `driver_machine.match_known`, the same technique as the price-key spy (`dry_driver.py:34-47`) | grep `Driver\.` and `driver\.[a-z_]+ =` over the owns: no assignment (positive control: `driver.stage_review_exhausted =` is found at `RM/scripts/tests/test_stage_critic_route.py:279`, as P1-b `:47` names it) |
| AR-18 (one output shape for detectors) | The walker prints the main pass's forms: `PASS <name>`, `FAIL <name> — <detail>`, `NOTE <name>: <detail>`, and `=== scenario dry-1: n/m ok ===` | e2e self-test output (DoD 4) |
| AR-20 (shrink-only ratchets) | No ratchet base changes. The printed `unwalked <group>` line is a NOTE, and the census keeps the ratchet (F-W9) | `dry_exits.py --check` stays at 0 discrepancies (DoD 3) |
| AR-22 (a field read has a producer) | If F-W4 (a): `state/dry-routes.jsonl` gets its producer (`dry_driver.py`) and its reader (`dry_world`) in ONE commit | pure-table row: a route row with no record -> red "route not observed" |
| AR-25 (every returned state has a move) | The walker is the detector: C2 and C3 per row | pure-table rows for C2 and C3 |

Not touched (one line each, as `architecture.md` "How a change walks" п. 2 asks): AR-1...AR-12 except AR-1 inside the test layer
(the reserved variant names and check ids are data tuples in one place, section 12), AR-14, AR-16, AR-19, AR-21, AR-23, AR-24
(C7 is not in this node, F-W13), AR-26, AR-27. The node adds no package code outside `scripts/tests/`.

### The checks this node adds or alters: owner (P27) and census class (AR-29)

`test_judgment_census.py` does not count `scripts/tests/` (P1-b `:71-73`). The classes are given for critic question 11.

| # | Check | Owner | Class |
|---|---|---|---|
| W-G | Row grammar: unknown field refused by name, closed reach/start/variant/check vocabularies, `words` and `words_file` exclusive | data (code) | shape |
| W-O | Every row has exactly one outcome, and a part with no rows is red | data | presence |
| C2 | The answered variant was offered and taken (F-W7) | data | xref |
| C3 | After the answer, the fingerprint differs from the one at the ask | data | shape |
| C4g | A gate-class row: the person's word passed the block and a new line exists in `state/passed-by-person.jsonl` | intent (owner: P13, FR-4); code checks only that the pass and the line exist | presence |
| C5 | The third identical ask, with nothing new given to the author | data | xref |
| C6 | At a `gate_A`/`gate_B` question in a row, the rehearsal's `gate_ready` is true | data | xref |
| C9 | (only if F-W13 (a)) among the options of a `stage_review_exhausted` ask there is a `rework_stage` whose `args.role` is the stage's author | data | xref |
| K15/E17 | A key row: the price key is observed, and the offered answers equal the key's price rows | data | xref |
| E18-row | Every stub journal line a row adds carries `run_class: dry` | data | presence |
| W-S | A start snapshot is unchanged after the row (tree hash) | data | xref |
| W-L | A label-ledger row that names neither `main/...` nor any walk row id is red in the census | data | xref |
| empty | (F-W8) The `empty` variant: the driver refuses the empty answer, and the question stays asked | data | presence |

Judgment (is the row a good case, is a red a bug, is the conductor's move sensible) is checked nowhere. It stays with P2-g, the
critic and live runs (P1-b `:89-90`).

---

## 2. Inventory, measured: what of the walker exists today

| Part | Where (file:line on BR) | What it does today | Usable by the walker as is? |
|---|---|---|---|
| Part grammar | `test_scenario_dry_1.py:44-50` `parse_part` | Accepts `main[:<type>]` only. Anything else -> stderr "unknown part ...; expected main or main:<type> (the walk rows are written by node N4)", exit 2 (S0R `:10-13`, S14R `:12-14`) | no: `exits:` is the gap |
| Entry | `test_scenario_dry_1.py:53-70` `main` | Without `--part`: census (`:27-33`) + forms grep (`:36-41`) + main pass. `--part main`: main pass only. Result kinds `note` -> `print("NOTE ...")`, others -> `harness.check` (`:64-68`) | the output form is reusable |
| World of the story | `dry_world.py:305-329` `build_story_world` | Fresh project, file ticket adapter, runner installed, `STORY_RUN_CLAUDE`=stub, `STORY_RUN_CLASS=dry` (`:322`), control file written (`:328`) | yes |
| Control file | `dry_world.py:266-270` `World.control(stub)` | Writes `{"task", "story"|"type", "stub": merge_stub(row stub, given stub)}`. It never writes a top-level `conductor`, which is the key the conductor stub reads (`dry_stub.py:97`, `:887`) | partly: a row cannot steer the conductor through it (item 4) |
| Snapshot | `dry_world.py:349-356` `snapshot` | Byte copy of the project into `world.snaps/<id>/<name>` plus `.dry-snapshot.json` with this process's `RUN_LABEL` (`:39`) | yes |
| Copy of a snapshot | `dry_world.py:359-374` `from_snapshot` | Missing -> `SnapshotError` "not found"; a foreign label -> `SnapshotError` "snapshot not from this run" (E16); copies to a temp dir, rewrites absolute paths except `events.jsonl` (`:333-346`), returns a `World` with `server=None` and **the main world's `snaps`** (`:374`) | yes, with one hazard: `World.close()` on a copy would `rmtree` the MAIN snapshots (`:276`). `run_row` avoids it with `harness.cleanup(copy.root)` (`:514`) (EW20) |
| Snapshot naming and timing | `dry_world.py:875-877` (main pass) | After each driver turn, every stage that is `done` and has no snapshot yet gets one, all at that moment. With `--max-boundaries 60` (`:868`) a turn runs until the next question. Measured: snapshots S0..S4 from 4 processes (N2g `:41`, `:43`) | partly: names mean "stage n is closed", not "at the border of n" (F-W6) |
| Snapshot immutability | `dry_world.py:610-622` `tree_hash`, `snapshot_red` | sha256 over sorted paths and bytes; red "snapshot changed by a row: <name>" | yes (used by `spike` `:663-672`) |
| One driver process | `dry_world.py:383-407` `drive` | Runs `dry_driver.py --project --task <args>`, stamps lines, kill on timeout -> `rc=-9` and a line naming the seconds | yes |
| Probe-row runner (N0) | `dry_world.py:488-514` `run_row` | N0's probe row (`start`, `stub`, `expect` kind, `answers`), always `--until gate_A --max-boundaries 12`, then one answer turn with `--max-boundaries 1`. No `seed`, no checks, no outcome forms beyond a text | no: it is the spike's, not §3.3's (S0R `:17`) |
| Main pass | `dry_world.py:840-1009` `main_pass` | Drives S0..S9, answers from `story.json` walk rows (`walk_answers` `:749-761`), C3 (`:898-908`), C5 (`loop_problem` `:797-807`, `author_hashes` `:810-815`), C6 (`gate_ready` `:764-794`), E18 (`:883-888`), reconcile of `main/...` ids only (`:951`), `after:` NOTEs for walk rows whose start was not made (`:980-993`), scoreboard (`:818-837`), then `world.close()` (`:1007-1008`) | the parts yes, the function no: it cannot stop early and it destroys its snapshots |
| Ledger reconcile | `known_red.py:130-152` `reconcile`; `load` `:72-111`; `pin_problem` `:114-127` | `True` green, anything else red; a ledger row not in `results` -> "unknown row" (`:147-149`) | yes, IF the caller passes only its own ids (the main pass filters by prefix, `:951`) |
| E15 rule "never expected red for the defect that made it unreachable" | nowhere: `known_red.py` has no `after` logic (read whole `:1-153`) | — | missing (F-W16) |
| Walk-row loader | `dry_exits.py:231-254` `load_walk_rows` | Reads `stories/dry-1/exits/*.json`; absent dir -> `{}`; id `<x>/<y>`; checks ONLY the census row keys (`:248` filters the row to `ROW_KEYS` `:42`), so an unknown walk-row field passes silently; an empty `rows` list passes | partly: grammar check missing (item 8) |
| Census over walk rows | `dry_exits.py:623-643` `_walk_problems` | A row's subject exists (price key, route, joint or kind); a walk row never carries a count reach; a census row claiming `seed`/`story` needs a walk row | yes |
| `unwalked` | `dry_exits.py:565-573` `_count_reach`, `:669-688` `_ratchets` | Counts census and walk rows whose `reach` is `unwalked`, summed over ALL groups, against the summed bases. No per-group figure exists anywhere | partly (item 10, F-W9) |
| `driven_keys` | `dry_exits.py:764-775` | A key is driven when every `<key>/<answer>` row has reach `story`/`seed` | yes; depends on the id form (F-W2 keeps keys bare) |
| Fingerprint, same ask | `dry_exits.py:820-865`, `:874-888` | §3.4 as built; "rounds unknown" note | yes |
| Census CLI | `dry_exits.py:1617-1653` | `--check`, `--selftest`, `--judge` | yes; `--selftest` gets the new rows |
| Price-key record | `dry_driver.py:34-47` `passing_spy` | Appends `{"key","answers"}` to `state/dry-priced.jsonl`; its docstring names "the walker's E17 ... key not observed" as the check that turns a gap red (`:13-14`). That check is written nowhere (section 14) | the producer yes; the reader is missing (item 3) |
| Stub control as built | `dry_stub.py:632-655` `stub_control` (`<role>`, `<role>@<stage>`, `<role>@<stage>#<window>`, plus `source_relevance`); `:409-415` `overrides_for` (`repair_on_round` is an INT call number); `:223` `ABSENT_JSON = {"$absent": true}`; `:91-115` `conductor_verdict` (`variant`, `action`, `options`, `execute`) | the grammar the stub really reads | yes, as the target of F-W1 (b) |
| Outcomes printed today | `test_scenario_dry_1.py:64-68`; `dry_world.py:956-962` | `PASS dry-1/main/S0`; `NOTE dry-1/main/known_red: known red: main/S5 -> P1B-9`; `NOTE dry-1/main/after: after:P1B-9: no snapshot for S5, ...` (N2g `:33-44`) | yes: the forms the walker reuses (axis 17) |
| `exits:` anywhere | — | none on BR (section 14); none on `origin/wip/p1b-*` (S0R `:18`) | — |
| Self-test group / seeds files | — | `fixtures/stories/dry-1/` holds `story.json`, `kit.json`, `impl.diff`, `ticket/`, `runners/` and no `exits/` or `seeds/` (section 14) | — |

What is missing for one exit row, end to end: (1) validate the row and its seed recipe BEFORE any world is built; (2) a
snapshot that exists in THIS process (a main-pass prefix); (3) copy it, write the row's control, including the conductor;
(4) run the seed (`drive_until` answering intermediate questions with the story's closed words, and `op` steps); (5) recognise that
the target question, route or joint has been reached, and observe the price key; (6) write the answer bytes and drive the
post-answer turns; (7) collect the facts (fingerprints, asks, priced record, stub lines, passed-by-person lines, gate rehearsal);
(8) judge the row's listed checks with a pure function; (9) print one outcome line and reconcile against the ledger, filtered to the
group's ids; (10) print the group's `outcomes` check and its `unwalked` NOTE; (11) hash the start snapshots afterwards.

---

## 3. The requirement as invariants (what must stay unreachable)

| # | Invariant | Where it is held |
|---|---|---|
| I1 | A row with no outcome never passes silently: each row prints exactly one of PASS / FAIL / NOTE(`known red`) / NOTE(`live_only`) / NOTE(`after:<node>`) / NOTE(`owner question Q<n> open`) / NOTE(`pending judge`), and a part whose rows printed fewer outcomes than rows is red | item 9 `outcomes` check |
| I2 | A row with no check never passes: an empty or absent `expect.checks` on a row that runs is refused before any world is built | item 8 |
| I3 | An unknown field of a row, of its `answer`, of its `expect`, or of a seed step is refused BY NAME before any world is built | item 8 |
| I4 | A row seeded from a snapshot never mutates the snapshot or the main-pass world: rows run on copies, the start tree hash is compared after each row, and `close()` is never called on a copy | items 5, 6; EW20 |
| I5 | A snapshot not made by this process is never a start (E16) | `from_snapshot` as is |
| I6 | A row of another group is never walked by this part: the part loads exactly `<exits-root>/exits/<group>.json`, and the ledger is filtered to that file's ids | items 2, 9 |
| I7 | `known_red` needs a ledger row: a red row with no ledger row is red ("new red"), and a green row with a ledger row is red ("stale") | `known_red.reconcile`, unchanged |
| I8 | A ledger row no part and no main pass can ever report (an orphan) is red in the census | item 11 |
| I9 | A row that could not start because its snapshot was not made is NOTE `after:<node>` only when the main stop is a ledger row. With no ledger row at the stop it is red | item 6 |
| I10 | A row is never expected red for the defect that made it unreachable (E15): a ledger row for `R` whose node equals the `after:<node>` that row `R` prints is red | item 9 (F-W16) |
| I11 | A key row whose key was not observed, or whose offered answers differ from the price rows, is red, never a guess from the text (E17, K15) | item 3 |
| I12 | A dry run is never counted live: a stub line a row adds without `run_class: dry` is red (E18) | item 3 |
| I13 | `unwalked` counts census entries (routes, joints, keyless kinds) of the group whose reach is `unwalked`, plus the group's walk subjects that miss a variant §3.3 demands. Price keys with no row at all stay with the existing census (P1-b `:233-234`, one road) | item 10 (F-W9) |
| I14 | The self-test group never counts toward the census, `driven_keys` or the ratchets: it lives outside `stories/dry-1/exits/`, the only directory those read (`dry_exits.py:38`, `:231-237`, `:764-768`) | item 12 |
| I15 | `--part main` keeps its behaviour: the same line set as before the refactor | item 1 |

---

## 4. Coverage: every element of the §3.3 grammar and every check assigned to exit rows

| Element (P1-b) | In this node? | Card item / test row, or where it goes |
|---|---|---|
| `id` `"<subject>/<variant>"` (§3.3 `:241-242`, `:253`) | yes | item 8: parse + subject resolution with the namespace of F-W2; table rows EW9, EW10 |
| variants: each `answer` of the key (`:243`) | yes | item 10: missing-variant count; table row |
| variant "free words" (`:243`) | yes (reserved name `free words`) | item 8 vocabulary; item 3 answer bytes; table row |
| variant "empty answer" (`:243`) | yes (reserved name `empty`) | item 7 check `empty` (F-W8); e2e self-test row `s1.review/empty` |
| E9 battery rows (`:243-246`, E9) | grammar only | item 8 accepts variants `words:<case>`; the content and C7 are N4's rows and F-W13 |
| route variant "code move" (`:246-247`) | yes (reserved name `code move`) | item 3 route observation (F-W4); table row |
| joint variants (silent) | fork F-W3 | item 8 vocabulary per F-W3 |
| keyless-kind variants, dynamic options (silent) | fork F-W15 | item 8 |
| `hook_layer` rows are not walked (`:247`) | yes | item 8 refuses a walk row with reach `hook_layer` (the census already does, `dry_exits.py:633-635`) |
| `start` `S0..S9` (`:254`) | yes | items 6, 7; EW11-EW13 |
| `start` `after:<id>` (`:254`) | fork F-W14 (recommend: drop) | item 8 refuses it per the recommendation |
| `seed` steps (`:255`, §4.3 `:447-450`) | yes, shape per F-W11 | items 5, 8 |
| `seed` `drive_until {stage, question}` | yes | item 5 |
| `seed` `op [script, args]` | yes | item 5, closed script list (section 12 S-4) |
| forbidden seeds (hand-written `asked`, `pipeline.json` stages, question files, an in-process `Driver`, §4.3 `:449-450`) | yes | item 5: `op` scripts from a closed list; no file write by the walker into the copy except `answer.md` and the control file |
| `answer.token / words / words_file` (`:256`) | yes | item 3 `answer_bytes`; EW14-EW16 |
| `stub.verdicts / conductor / overrides / repair_on_round` (`:257-259`) | yes, in the grammar chosen at F-W1 | item 4 |
| `expect.checks` (`:260`) | yes | items 7, 8 |
| `expect.owner_quote {text, carrier}` (`:260`, E14) | grammar yes; the expectation no | item 8: when present, `text` non-empty and `carrier` `<path>:<line>` resolving to an existing file with that many lines; the expectation itself is F-W13 (C8) |
| `reach story | seed | live_only | after:<id>` (`:261`) | yes | item 6 (F-W10 for static `after:`) |
| `why_unreached` (`:262`) | yes | item 8: required for `live_only`/`after:`; refused on a row that runs (section 12 S-6) |
| `repair_on_round` semantics (`:265-267`) | as built (F-W1) | item 4 |
| C2 (§1 `:78`, §3.4 `:302-306`) | yes, as defined in F-W7 | item 7; table rows |
| C3 (`:79`, §3.4) | yes | item 7; table rows incl. "rounds unknown" -> NOTE, not PASS C3 (P1-b `:300-301`) |
| C4g gate class (`:80`, §3.6, E10) | yes | item 7: needs `class_of(subject) == "gate"`, else the row is refused; table rows |
| C4z bans (`:81`) | not in this node: a census data check, already `dry_exits.ban_doors` (`:536-545`), no row (P1-b `:247`) | — |
| C5 (`:82`, §3.4 `:279-285`) | yes | item 7 reuses `loop_problem`; table rows |
| C6 (`:83`, N3 item 4) | yes, at gate questions inside a row | item 7 reuses `gate_ready` on the row's copy (own `snaps`, EW20) |
| C7 words whole (`:84`, AR-24, N4 DoD E9) | not in this node (F-W13) | a row listing it prints NOTE `pending judge C7`, not reconciled |
| C8 owner quote (`:85`, E14, F9) | grammar only (above); the expectation not in this node (F-W13) | — |
| C9 FV1-6 (`:86`, §9.3 `:831`) | fork F-W13 (recommend: in this node) | item 7 |
| C10 FV1-19 (`:87`, §9.3 `:835`) | not in this node (F-W13): reachable only after S5 (`after:P1B-9`) | NOTE `pending judge C10` |
| K15 in process (§3.2 `:194-196`), E17 | yes | item 3 |
| E18 per row (§4.4 `:457-460`) | yes | item 3 |
| E16 snapshot of another run | yes (as built) | item 6 |
| E15 rule on labels | yes (F-W16 recommends: in the walker) | item 9 |
| E6 cap per row (`:483`) | yes, value per F-W17 | item 5; EW22, EW23 |
| E20 (`driven` needs every answer executable) | unchanged (`driven_keys`) | — |
| E22 owner questions | fork F-W12 | item 8 |
| §3.5 scoreboard after each row | yes | item 6 calls `scoreboard(copy, line)` with the row-prefixed name (the NOTE "not wired" until P1-v) |

---

## 5. The card N4w (for a builder weaker than the designer)

Order: N3 (done on `wip/p1b-n3`) -> **N4w** -> the five N4:<group> parts (parallel) -> N4c -> N5. Branch `wip/p1b-n4w` from
`wip/p1b-n3`. The worktree root is `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w`. The card follows the RECOMMENDED
option of every fork in section 11. Where a fork changes an item, the item says so.

| # | File, function | Expected behaviour | Test row that proves it |
|---|---|---|---|
| 1 | `dry_world.py`: new `drive_main(world, answers, *, stop_after=None, line) -> dict`; `main_pass` rewritten to call it | Moves the turn loop of `main_pass` (`:866-945`) into `drive_main` unchanged in behaviour. `stop_after="S<n>"` ends the loop after the turn in which snapshot `S<n>` was made (or when the loop ends earlier for any reason it ends today). Returns `{"state", "stop", "first_ref", "spans", "turns", "asks", "gates", "class_seen"}`. `main_pass` keeps everything after the loop (reconcile, notes, scoreboard, `close`). `main_pass` NEVER passes `stop_after` | DoD 6: `--part main` prints the N2g `:33-44` line set (PASS S0..S4, PASS gate_A, NOTE known red main/S5, stop, snapshots S0..S4, after, time); pure-table row: `drive_main` returns at once when a `stop_after` snapshot already exists (fake driver: section 7 note on the fake) |
| 2 | `test_scenario_dry_1.py`: `parse_part(text) -> (kind, label)`, `main(argv)`, new `exits_part(group, exits_root, ledger)` | `--part main[:<type>]` exactly as today. `--part exits:<group>` with a non-empty `<group>` matching `^[a-z0-9][a-z0-9-]*$` -> `exits_part`. `exits:` with an empty or malformed group -> stderr naming the known parts and the groups found in `<exits-root>/exits/`, exit 2 (the form of today's `:48-49`). New options `--exits-root` (default `fixtures/stories/dry-1`) and `--ledger` (default `fixtures/driver-exits/known_red.json`), legal only with `exits:` (else exit 2 naming the option). **POSITIONAL**: the `exits:` branch sits BEFORE the census and main pass of the default mode, and never runs them: a part judges its rows only. The invariant: the default mode (no `--part`) stays census + forms grep + main pass, byte-for-byte the same calls, so the `full` canon job is unchanged (P1-b §10, `:853-854`) | e2e DoD 5: `exits:` -> rc 2; `exits:nosuch` -> rc 2 naming the groups; `--exits-root` without `exits:` -> rc 2; pure-table rows for `parse_part` |
| 3 | `dry_world.py`: new `row_facts(copy, row, subject, before) -> dict` and `answer_bytes(row, story_dir) -> bytes`; `dry_driver.py` (F-W4 (a)): `route_spy(real, sink)` on `driver_machine.match_known`, writing `{"route": name}` to `state/dry-routes.jsonl` after a non-None return | `answer_bytes`: `token` only -> `token + "\n"`; `words` only -> the words encoded UTF-8 exactly; `token` and `words` -> `token + "\n" + words`; `words_file` -> the file's raw bytes (BOM and CRLF kept), the path relative to the story folder and resolving INSIDE it; all three null -> `b""` (legal only for variant `empty`, item 8). `row_facts` collects, after the post-answer turns: fingerprints at the ask and after each turn; the asks (same record as `main_pass` `:912-920`); the last `dry-priced.jsonl` records added by this row; the stub journal lines added by this row; the `passed-by-person.jsonl` lines added; the `dry-routes.jsonl` lines added; the gate rehearsals done; the driver's first refusal line | pure-table rows EW14-EW16 (answer bytes, incl. `..` and absolute `words_file` refused); a table row for the route spy: the spy returns exactly what the real function returns and records only after a non-None result (the same two properties `dry_driver.py:34-47` holds for prices) |
| 4 | `dry_world.py`: `World.control(stub=None, conductor=None)` | Writes the row's control in the grammar chosen at F-W1. Recommended (b): the row's `stub` is merged over the story's `stub` by `merge_stub` (`:152-157`, as today); a `conductor` key of the row's `stub` is removed from the table and written as the control's TOP-LEVEL `conductor` (the key `dry_stub.conductor_verdict` reads, `dry_stub.py:97`). A row without `stub` writes the story's control unchanged | pure-table row: a row `stub` with `conductor: {"variant": "go on"}` produces a control whose top level holds `conductor` and whose `stub` holds no `conductor` key; a row without `stub` produces the same bytes as `build_story_world`'s control |
| 5 | `dry_world.py`: new `run_seed(copy, recipe, answers, *, cap) -> (reached, detail)` | Steps in order. `drive_until {"stage": "S<n>", "question": "<subject>"}`: if the copy ALREADY holds that question pending (`driver-state.json` `asked` kind or the last priced key equals it), it is reached with no driver run (EW12). Otherwise one driver process per turn (`--max-boundaries 60`, as the main pass); an intermediate question is answered with the story's closed words (`walk_answers`, keyed by `(stage, kind)`, the main pass's one source, A1-E3); an intermediate question with no closed words, the conductor, a driver exit with no new question, or `MAX_TURNS` -> not reached, naming what was met. `op ["<script>", args...]`: `<script>` must be in the closed list of section 12 S-4, run as a process in the copy (`run_script` form, `STORY_RUN_CLASS=dry` in its env), exit != 0 -> not reached with the stderr cut at 400. Every turn is bounded by the per-row cap (F-W17); over the cap -> not reached, "over the cap: <s> s (cap <c> s)" | pure-table rows with a fake driver: already pending -> reached with 0 turns; intermediate answered -> reached; intermediate with no words -> not reached naming the kind; `op` with a script not on the list -> refused at validation (item 8); cap AT (exactly the cap: still running is allowed) and BEYOND (cap + 1 s -> not reached) |
| 6 | `dry_world.py`: new `walk_exits(story_id, rows, seeds, ledger_path, line, *, exits_label)` | (a) `stop_after` = the latest `start` among the group's runnable rows. `S0` is the floor. (b) build the story world once, `drive_main(..., stop_after)` (main-pass lines of the prefix are NOT printed as PASS/FAIL, only one NOTE `exits:<g>/prefix: reached S<k> in <s> s; snapshots <list>`). (c) Print the snapshot index (item 7 below). (d) Hash every start snapshot. (e) For each row in file order: not runnable (`live_only`, static `after:`, owner question) -> its NOTE, no world. Runnable with its start snapshot made -> copy (with its OWN `snaps` dir for gate rehearsals), `World.control`, `run_seed`, answer, post-answer turns (item 7), `row_facts`, `judge_row`, scoreboard on the copy, `harness.cleanup(copy.root)` and the copy's own `snaps` removed (never `close()` on a copy, EW20). Start snapshot not made: if the prefix stop is a `main/S<n>` ledger row -> NOTE `after:<node>`; else FAIL "start S<n> not made and the main pass stopped at <stage> with no known_red row" (I9). (f) After all rows: `snapshot_red` per start; a change -> FAIL naming the row that ran last on that snapshot. (g) `world.close()` | e2e self-test (DoD 4): rows of each outcome kind; pure-table rows for (e) branches with fake facts |
| 7 | `dry_world.py`: post-answer turns inside `walk_exits`; `dry_exits.py`: new pure `judge_row(row, facts, *, classes, prices, class_of_subject) -> Outcome` | Post-answer: write `answer.md` with `answer_bytes`, then turns of `--max-boundaries 1`, at most `POST_TURNS = 4` (section 12 S-3), stopping early when the fingerprint changed AND a new or different ask appeared, or the driver exited with no new question. C5 needs 3 asks, so the walker answers a repeated identical ask with the same bytes (the person repeating), up to the cap. `judge_row` evaluates EXACTLY the listed `expect.checks`, in order: C2 (F-W7 (a)): the answered token is in the ask's offered set (normalised by `DriverDialog.s0_normalize`), the driver's answer record exists for that ask (`driver-answers.jsonl`, `question_sha` of the ask), and no conductor call with `why: unread_answer` followed. For a refusal state, at least one variant other than `stop` changed the fingerprint (P1-b `:302-306`): this cross-row part is judged at group level (item 9). C3: fingerprint after != at the ask; the facts note "rounds unknown" -> the C3 result is NOTE "rounds unknown", never PASS (P1-b `:300-301`). C4: the subject's class (via `class_of`) is `gate` (else the row is refused at validation) AND at least one new line in `passed-by-person.jsonl` after the answer. C5: `loop_problem(asks)` is empty. C6: every gate question the row met has `gate_ready is True`. C9 (F-W13 (a)): among the options of the `stage_review_exhausted` ask (`driver-state.json` `asked.options`) there is a move `rework_stage` whose `args.role` equals the stage's author role (`stages.json`); an option without `args.role` counts as missing ("executor not named", FR-42). `empty` (F-W8 (a)): the answer turn printed the driver's refusal of an empty answer, and the same ask is still pending. Always, whatever the list: K15/E17 for a key subject (a priced record with the row's key was added; its `answers` set equals the price rows' `answer` set), E18 (every added stub line has `run_class == "dry"`), the route record for a route subject (F-W4). Listed and not implemented (`C7`, `C8`, `C10`) -> outcome NOTE `pending judge <ids>`, not reconciled (F-W13). A failing check -> FAIL naming the check and the evidence (cut at 300, the main pass's `cut`) | pure-table rows, one per check and per branch: pass, fail, rounds unknown -> NOTE, C4 on a non-gate subject refused, priced record absent -> FAIL "key not observed", answers differ -> FAIL naming the difference, stub line with `run_class: ""` -> FAIL, unimplemented check -> NOTE, unknown check id -> refused at validation |
| 8 | `dry_exits.py`: `WALK_ROW_KEYS`, `ANSWER_KEYS`, `EXPECT_KEYS`, `SEED_STEP_KEYS`, `CHECK_IDS`, `RESERVED_VARIANTS`; new `walk_row_problems(path, row, *, universe, seeds) -> list`; `load_walk_rows(walk_dir, *, strict=False)`; new `load_seeds(path) -> dict` | Grammar of section 8 below. `load_walk_rows(strict=True)` (the walker's call) refuses: an unknown field at any level, by name; an id that does not resolve to exactly one subject under the F-W2 namespace; a variant outside the subject's vocabulary (F-W2/F-W3/F-W15); `start` not `S0`..`S9`; a runnable row with an empty or absent `expect.checks`; an unknown check id; C4 on a non-gate subject; `words` with `words_file`; all three answer fields null on a variant other than `empty`, or any of them non-null on `empty`; `seed` naming a recipe absent from `seeds/<group>.json`; `owner_quote` without both fields or with a carrier that does not resolve; `why_unreached` on a runnable row; an EMPTY `rows` list. `strict=False` (the census, `check()` and `driven_keys`) gains exactly two refusals: the empty `rows` list and an unknown top-level row field, so the census and the walker cannot disagree on whether a file is a group (one road). All refusals happen BEFORE any world is built (the E-R3 form of R3) | pure-table rows EW1-EW10, one per refusal, each with the id and the field in the message |
| 9 | `dry_exits.py`: new `judge_group(outcomes, ledger_path, ids) -> Verdict`; `test_scenario_dry_1.exits_part` | Builds `results = {row id: True|False}` from the rows that RAN (PASS -> True, FAIL -> False). Rows with a NOTE outcome are not in `results`. Reconciles with `known_red.reconcile(results, ledger filtered to the ids of THIS group's file)`. Prints PASS for green rows, NOTE `known red: <id> -> <node>` and FAIL for its problems (the main pass's forms, `dry_world.py:956-962`). E15 (F-W16 (a)): a ledger row for an id whose outcome is NOTE `after:<node>` with the same node -> FAIL "a row is never expected red for the defect that made it unreachable: <id>". Then one check `dry-1/exits:<g>/outcomes`: PASS when every row of the file printed exactly one outcome, with the count per kind in the detail. The C2 refusal-state rule: for a subject whose rows all ran, if every variant except `stop` left the fingerprint unchanged -> FAIL "alive only stop: <subject>" (P1-b `:304-305`) | pure-table rows: a ledger row of another group is NOT reported as "unknown row" by this part; a red row with a ledger row -> NOTE known red; green + ledger -> FAIL stale; E15 conflict -> FAIL; "alive only stop" -> FAIL; a row with two outcomes -> FAIL `outcomes` |
| 10 | `dry_exits.py`: new `group_unwalked(group, census, walk_rows, prices) -> (count, lines)` | Counts (F-W9 (a)): census entries of `driver-exits/<group>.json` with reach `unwalked`, plus the subjects of this group's walk file that miss a variant §3.3 demands (for a key: each price `answer` + `free words` + `empty`; for a code route: `code move`; joints and kinds per F-W3/F-W15). Printed as NOTE `dry-1/exits:<g>/unwalked: <n> (census unwalked <a>: <names>; variants without a row <b>: <ids>)`. No census file for the group (the self-test group) -> NOTE "no census file for group <g>: unwalked not counted" | pure-table rows: a key with answers a, b and only `k/a` written -> count 3 (b, free words, empty); census row `unwalked` -> counted; no census file -> the NOTE |
| 11 | `dry_exits.py` `check()`: new `_ledger_orphans(ledger, walk, census)` | A ledger id that is neither `main/<anything>` nor a walk row id in `stories/dry-1/exits/*.json` -> problem "label ledger row <id> names no walk row and no main stage; no part can ever report it - rename or remove it" (I8). The self-test ledger is a different file and is never read by `check()` | pure-table row on a temp tree: an orphan id -> red; a `main/S5` id -> not red; an id of a written walk row -> not red |
| 12 | `fixtures/stories/dry-1/selftest/exits/selftest.json`, `.../selftest/seeds/selftest.json`, `.../selftest/known_red.json` | The self-test group, real rows proving each outcome kind on today's main pass (section 7, DoD 4). It is read only with `--exits-root .../selftest`. It is inside `fixtures/stories/dry-1/`, so the keep row's `covers` already names it (`test-layers.json:5113`) and no `test-layers.json` edit is needed. It is outside `stories/dry-1/exits/`, so the census, `driven_keys` and the ratchets never read it (I14) | DoD 4 output |
| 13 | `changelog.d/p1b-n4w-exit-walker.md` | One English fragment: the walker part and its grammar | `selftest.py --lang` green |

### 5.1 Fakes for the pure table

`judge_row`, `judge_group`, `group_unwalked`, `walk_row_problems`, `answer_bytes` and `parse_part` are pure: their table rows feed
synthetic facts and files in a temp dir, so no driver runs. `run_seed` and `drive_main` take an injectable `drive` callable
(default `dry_world.drive`). Their rows pass a fake that returns scripted `Run` objects and writes scripted question records into a
temp task root. This is the same injection `dry_stub.automator_branch` uses (`run=run_script`, `dry_stub.py:463`). One process,
one temp tree per row, so TESTING.md `:124-125` is kept for the table.

### 5.2 Self-test group rows (item 12): what each proves and why it does not count

| Row id (F-W2 (a) form) | start | Shape | Expected outcome on today's main pass | Proves |
|---|---|---|---|---|
| `s1.review/go on` | S0 | seed `[]` (the S0 snapshot already holds the `s1_review` question pending, section 0 fact 2); answer token `go on`; checks `["C2", "C3"]` | PASS | the runnable road, K15/E17 on the observed key `s1.review` (N2g: the main pass observes it), C2, C3 |
| `s1.review/empty` | S0 | seed `[]`; all answer fields null; checks `["empty"]` | PASS if F-W8 (a), the driver refusing an empty answer (P1-b E9: "is empty") | the `empty` variant |
| `s1.review/stop` | S0 | seed `[]`; token `stop`; checks `["C3"]`; the self-test ledger holds `"s1.review/stop": {"node": "P1B-9", "raised_by": "N4w self-test: proves the known_red path; a held stop leaves the fingerprint unchanged"}` | NOTE `known red: s1.review/stop -> P1B-9`, IF `stop` leaves the fingerprint unchanged. If the builder measures that it changes it, the builder picks another variant that is red today and reports it; never a hand-made red | reconcile through the ledger file `--ledger` names |
| `kind:conductor/stage_review_exhausted:rework_stage` | S2 | reach `live_only`, why "self-test: proves the live_only NOTE" | NOTE `live_only: ...` | no world for a non-runnable row |
| `s8.delivery.no/go on` | S8 | reach `seed`, seed recipe `to-s8` with one `drive_until` step | NOTE `after:P1B-9: its start snapshot S8 was not made` | the TEMPORAL `after:` road (E15) |

Why it does not count toward `unwalked`, the census, `driven_keys` or the ratchets: those read only `fixtures/stories/dry-1/exits/`
(`dry_exits.py:38`, `:231-237`, `:764-768`) and `fixtures/driver-exits/<group>.json` (`:180-213`); there is no
`driver-exits/selftest.json`, so item 10 prints "no census file". Why not a built-in group inside the code: rows are data (AR-1
inside the test layer) and the e2e proof must use the same loader as N4's files (one road).

---

## 6. Edges (behaviour and the invariant each protects)

| # | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| EW1 | `exits/<group>.json` ABSENT (TEMPORAL: before N4 writes it) | FAIL `dry-1/exits:<g>/rows: <path> is absent; expected the walk rows of group <g> (node N4:<g> writes them)`; no world is built; rc 1 | a part never passes on nothing (I1) |
| EW2 | `exits/<group>.json` with `"rows": []` | refused by the loader (item 8) naming the file, in both the walker and the census | an empty group says nothing (AR-28; the twin of `_empty_problems`, `dry_exits.py:173-177`) |
| EW3 | Unreadable or invalid JSON, or a duplicate key | FAIL naming the file and the JSON error (the `_read_json` form) | unknown is never a pass (E7) |
| EW4 | Unknown field at any level of a row | FAIL naming the row id and the field and listing the allowed fields | a mistyped field is never silently ignored (I3) |
| EW5 | `seed` names a recipe absent from `seeds/<group>.json`, or the seeds file is absent while a row names a recipe | FAIL naming the row, the recipe and the file, before any world is built | a row never runs on a seed nobody wrote |
| EW6 | Unknown group name (`exits:nosuch`): neither `<exits-root>/exits/nosuch.json` nor `driver-exits/nosuch.json` exists | rc 2 naming the groups found in both directories | a typo never runs another group (I6) |
| EW7 | A group with a census file but an absent walk file | as EW1 (FAIL), plus the `unwalked` NOTE with the census count | the gap is printed with its size |
| EW8 | A row id that resolves to two subjects (point (a): `s1_gap` is both a route and a kind) | under F-W2 (a) impossible by grammar; a bare id that is not a price key -> refused "a route, joint or kind id needs its namespace `route:`/`joint:`/`kind:`" | one id, one subject (known_red ids stay unambiguous) |
| EW9 | Subject not in the code (a stale key or route) | refused naming the subject (the census message, `dry_exits.py:631-632`) | — |
| EW10 | Variant outside the subject's vocabulary (e.g. `s1.review/maybe`) | refused naming the allowed variants | a row never "drives" an answer the key does not offer |
| EW11 | TEMPORAL: `start` S5..S9 while the main pass stops at `known_red main/S5` (P1B-9, `known_red.json:4`) | the prefix stops at S4 (the stop is not reached by `stop_after`, the loop ends on its own); NOTE `after:P1B-9: its start snapshot S<n> was not made`. After P1B-9 is fixed: the snapshot exists in the same run and the row runs, with no edit (E15) | an unreachable row is never PASS, and runs by itself once it is reachable |
| EW12 | The start snapshot already holds the target question pending (section 0 fact 2) | `drive_until` is reached with zero driver runs | the walker does not drive past its target |
| EW13 | Start snapshot not made and the main stop has NO ledger row | FAIL "start S<n> not made and the main pass stopped at <stage> with no known_red row" | I9 |
| EW14 | `words_file` absolute, containing `..`, resolving outside the story folder, or absent | refused naming the path | a row never reads outside its story |
| EW15 | `words` and `words_file` both set | refused | one answer, one source |
| EW16 | All answer fields null on a variant other than `empty`, or a field set on `empty` | refused | an empty answer is only ever the `empty` variant |
| EW17 | `drive_until` meets an intermediate question with no closed words in `story.json` | the row's outcome is FAIL "seed did not reach <subject>: met <kind> at <stage> with no answer in story.json" (no ledger match is possible unless N4 labels it) | a seed that does not reach is never PASS and never silent |
| EW18 | Target reached, but the observed price key differs from the row's key (`s5.nobody_*`-style sets, P1-b F10 (b)) | FAIL "key not observed: expected <k>, observed <k2>" | a row never drives another key (E17) |
| EW19 | `rounds unknown` in the fingerprint notes (`dry_exits.py:845-846`) | the C3 result is NOTE "rounds unknown"; a row whose only check is C3 gets outcome NOTE, not PASS | AR-28, P1-b `:300-301` |
| EW20 | A copy's lifecycle | the walker removes a copy with `harness.cleanup(copy.root)` and its own `snaps` dir; `World.close()` is never called on a copy (on today's `from_snapshot` copy it would delete the main snapshots, `dry_world.py:276`, `:374`) | I4 |
| EW21 | A row changes its start snapshot (a path taken from the un-rewritten `events.jsonl`, R3 E-R8) | FAIL "snapshot changed by a row: <id>", and the hash is re-taken so later rows are judged on their own | I4 |
| EW22 | LIMIT, per-row cap AT the value | a row finishing at exactly the cap is judged normally | the cap is a ceiling, not a target |
| EW23 | LIMIT, per-row cap BEYOND (cap + 1 s) | the driver is killed (`drive` `rc=-9`); outcome FAIL "<id>: over the cap <c> s at <phase>" | a row never drops out silently on a timeout (E6) |
| EW24 | LIMIT, `POST_TURNS` = 4 reached with neither a change nor a third identical ask | outcome FAIL "<id>: 4 post-answer turns with no new ask and no loop" | a long tail is never cut into a pass |
| EW25 | LIMIT, `MAX_TURNS` (40, `dry_world.py:709`) in `run_seed` | not reached, naming the limit | the same cap as the main pass (one road) |
| EW26 | CONFLICT: a check listed in `expect.checks` that is not implemented (C7, C8, C10) vs "every row has an outcome" | outcome NOTE `pending judge <ids>`; not in `results`; the other listed checks are still computed and printed in the NOTE's detail | a row is never green on an unjudged check (F-W13) |

Where the part dispatch sits (POSITIONAL, item 2): the `exits:` branch comes BEFORE the default mode's census and main pass and
returns without running them. The invariant: the default mode, which the `full` canon job runs, is byte-for-byte the same; an exits
part never prints `PASS dry-1/main/...` (its prefix is a NOTE), so no main-stage verdict is given twice in the canon (P1-b §10,
`:853-854`).

---

## 7. DoD: verification commands, time, and what the canon judges

Run from the worktree root `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4w` unless the command says otherwise.

1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`, output attached. Expected:
   `keep test_scenario_dry_1.py` for the four `.py` files and the self-test folder (the keep row covers them,
   `test-layers.json:5101-5115`). That file's DEFAULT mode (census + main pass, ~381 s, N2g `:43`) is over the 5-minute line of
   builder-rules 7b `:30-31`: it is judged by the batch canon and NOT run locally. The report says so in one line.
2. `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest`: every row PASS, including the new rows of items 1, 2,
   3, 5, 7, 8, 9, 10, 11 (section 5). Expected well under a minute (no driver; estimate, not measured).
3. `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check`: `0 discrepancies`; the NOTE "walk rows: none" still
   printed (the stricter loader on today's absent `exits/`).
4. `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:selftest --exits-root ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/selftest --ledger ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/selftest/known_red.json`:
   the lines `NOTE dry-1/exits:selftest/prefix: ...`, the snapshot index NOTE, `PASS dry-1/exits:selftest/s1.review/go on`,
   `PASS .../s1.review/empty` (F-W8 (a)), `NOTE .../known_red: known red: s1.review/stop -> P1B-9`,
   `NOTE .../kind:conductor/stage_review_exhausted:rework_stage: live_only: ...`, `NOTE .../s8.delivery.no/go on: after:P1B-9: ...`,
   `PASS dry-1/exits:selftest/outcomes`, `NOTE .../unwalked: no census file for group selftest: unwalked not counted`, and
   `=== scenario dry-1: n/n ok ===`, rc 0. **Time: estimate, not verified.** The prefix to S0 is the main pass's first turn (the
   N3 note puts the first stop at 48 s, `selftest.py:115-116`), plus three short rows of at most 1 + 4 single-boundary turns each.
   I expect 60-120 s. The report gives the measured seconds. Over 120 s, the builder stops and reports it, with the per-phase
   seconds (F-W17).
5. Grammar of the part, each under a few seconds: `... test_scenario_dry_1.py --part exits:` -> rc 2; `--part exits:nosuch` -> rc 2
   naming the groups; `--part main --exits-root x` -> rc 2; `--part exits:s0` (no walk file yet) -> FAIL EW1, rc 1.
6. `--part main` once on the final state (~381 s, N2g precedent `:47`), with the line set of N2g `:33-44`. This is over the minute
   and is fork F-W18: the Lead may move it to the canon.
7. `( cd ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )`: green (the changelog fragment, English, no
   Cyrillic in the package files).
8. Grep checks with positive controls (AR-17, AR-29 rows of section 1), output attached.
9. The commit message carries `architecture: AR-28, AR-29, AR-13, AR-15, AR-17, AR-18 -- <how kept>` and a `judgment:` line
   (`tools/architecture_gate.py`), plus the FR walk in the report (sections C, D, E, G apply; A, B, F: one line each).

What the batch canon judges instead: the default mode of `test_scenario_dry_1.py` (job `full`); the `exits:<g>` parts of the
five N4 groups in job `dry-story` (N5, after N4c). The builder runs neither CI nor mutations (PROJECT.md п. 13).

`--part` grammar vs the schedule rows (N3 items 6-7): **not owned, unchanged, and why.** `selftest.py` runs test files without
arguments, so `TEST_TIMEOUTS["test_scenario_dry_1.py"] = 900` (`selftest.py:117`) and `slow_tests.json` `51.0` (`:119`) time the
DEFAULT mode, which this node leaves unchanged (item 2, POSITIONAL). The `exits:` parts run only in job `dry-story`, which has its
own cap (N5). The keep row `test_scenario_dry_1.py` (`test-layers.json:5101-5115`) already covers `tests/dry_exits.py`,
`tests/dry_world.py`, `tests/dry_driver.py` and `scripts/tests/fixtures/stories/dry-1` (which holds the self-test folder), so no
`covers` edit is needed. One stale figure is noticed and not widened: `slow_tests.json` says 51.0 s while N2g measured 381.2 s for
`--part main`. That is queue line Q-3.

---

## 8. The row grammar the walker enforces (on the recommendations)

```
exits/<group>.json:
{"schema": 1, "group": "<group>",                       # group == the file stem, else refused
 "rows": [ {                                            # non-empty
   "id": "<subject>/<variant>",                         # subject: a price key (bare) | route:<name> | joint:<check> | kind:<kind>   (F-W2 (a))
   "start": "S0".."S9",                                 # F-W14 (a): no after:<id> here
   "seed": "<recipe id>" | null,                        # F-W11 (a): a name in seeds/<group>.json; null = the snapshot as it is
   "answer": {"token": str|null, "words": str|null, "words_file": str|null},
   "stub": { <the control grammar as built, F-W1 (b)>, "conductor": {...} },     # optional
   "expect": {"checks": [<CHECK_IDS>...], "owner_quote": {"text", "carrier"}|null, "owner_question": "Q<n>"|null},   # owner_question: F-W12 (a)
   "reach": "story" | "seed" | "live_only" | "after:<NODE>",
   "why_unreached": str|null } ]}

seeds/<group>.json:
{"schema": 1, "group": "<group>",
 "recipes": {"<recipe id>": [ {"drive_until": {"stage": "S<n>", "question": "<subject>"}} | {"op": ["<script>", "<arg>", ...]} , ... ]}}

CHECK_IDS = C2 C3 C4 C5 C6 C9 empty   (implemented)   +   C7 C8 C10   (pending judge, F-W13)
RESERVED_VARIANTS = "free words", "empty", "code move", "words:<case>"
variants of a key = its price `answer`s + the reserved ones; of a route with a code move = "code move"; of a route with ask_person = like a kind;
of a joint = F-W3 (a) "repair" | "no repair" | "word"; of a keyless kind = F-W15 (a) "<why or state>:<token>" + "free words" + "empty"
```

`reach` vs execution: `story` and `seed` run in the same way (one road); `live_only`, static `after:` and rows with
`owner_question` print their NOTE and do not run.

---

## 9. The four N4:<group> cards once the walker exists (short delta; owns unchanged)

Applies to `s0`, `s1-s4`, `gates`, `s5`, `s6-s9` alike:
- given += this spec (accepted path) §8 (the row grammar as decided) and §5.2 (the self-test rows as a worked example);
  `fixtures/stories/dry-1/selftest/` (read-only).
- DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:<group>`: every row of the group has an
  outcome (`PASS dry-1/exits:<group>/outcomes`); no FAIL other than rows the part's report lists for a ledger label (id -> finding);
  the NOTE `unwalked` shows 0; plus `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` with 0 discrepancies
  (the group's census rows moved from `unwalked` to `seed`/`story`/`live_only`, and the ratchet bases lowered in the same file).
  Time: each part pays its main-pass prefix to its latest `start` (F-W5 (a)); the s5 and s6-s9 parts today stop at the S4 prefix
  and print `after:P1B-9` for every row (EW11). Their local run is therefore mostly the prefix. Expected seconds: estimate,
  measured by the part.
- edges: += EW11, EW12, EW17, EW18 (what the part must expect from the walker).
- s1-s4 specifically: rows for states between S1 and S4 start at `S0` (section 0 fact 2, the coordinator's point (d)), unless F-W6
  (b) is taken. `kind:questions` raised at `driver_machine:_act_wait_existing_job` (point (e)) is the part's own call (likely
  `live_only`), not the walker's.
- the N4 card's group list (P1-b `:636`) names price keys (`s3.grounding_*`), which by design are never `driver-exits` entries
  (P1-b §3.2 `:215`), and `conductor/stage_review_exhausted`, a kind row with a why-variant (F-W15). Point (c) is a wording gap in
  that list, not a registry defect: section 10.

---

## 10. The coordinator's extra input (a)-(e), each checked against the registry

| Point | Checked against | Finding | Where covered |
|---|---|---|---|
| (a) `s1_gap`, `s1_review` are both a route and a keyless kind | `driver-exits/s1-s4.json:5-12` (routes) and `:56-70` (kinds): confirmed | the bare-id grammar `<subject>/<variant>` cannot tell them apart; known_red ids would be ambiguous | F-W2 (namespace), EW8 |
| (b) wildcard joints | `s1-s4.json:27-38`; `references/stage-joints.json:398, 475, 501, 547`: `*` is LITERAL in the check id (a joint covering a detector's whole family), so the census matches it exactly | §3.3 does not say what the variants of a joint are, nor how a `*` joint is observed | F-W3, F-W4 |
| (c) card names `s3.grounding_*` and `conductor/stage_review_exhausted`; the registry holds neither | `question-prices.json:250, 254, 258, 262`: `s3.grounding_coverage*` and `s3.grounding_refactoring` are PRICE KEYS; P1-b `:215` keeps price keys out of `driver-exits`; `conductor` is a kind (`s1-s4.json:41-47`) and `stage_review_exhausted` is one of the 8 `why` values of the seam (P1-b `:164`) | no disagreement of the registry with the code. The N4 card's prose list mixes price keys, kinds and why-states; a walk row for `conductor` in the why `stage_review_exhausted` needs a variant form | F-W15; section 9 |
| (d) S1 rows need snapshot S0 | `dry_world.py:868, 875-877`; N2g `:41`: snapshots are taken at turn end; S0 = the world at the `s1_review` question | confirmed, and it extends to S2-S3 (S1..S3 snapshots are the same world at `gate_A`) | section 0 fact 2, F-W6 |
| (e) `questions` has a second raise site that waits on an existing job | `s1-s4.json:51-54` | a seed for that site likely needs a live dispatch | the N4 part's call (reach `live_only`), not the walker's; section 9 |

---

## 11. Forks for the Lead (options, recommendation, error direction)

**F-W1. The `stub` grammar: P1-b §3.3 vs the control the stub reads.** §3.3 (`:257-259`): `stub.verdicts {"<stage>/<role>": v}`,
`stub.overrides {form: {field: value|"ABSENT"}}`, `stub.repair_on_round {"<stage>/<role>": {field: value}}` ("on round n+1 the role
writes this field so"). As built: a table keyed `<role>[@<stage>[#<window>]]` with per-role `verdict`, `overrides`
(`{"$absent": true}`), `repair_on_round: <int call number>` (from call n on, the overrides are dropped), `result_text`, `files`,
`grounding`, `manifest_fragments` (`dry_stub.py:632-655`, `:409-415`, `:223`; `story.json:7-80`), and the conductor at the control's
top level (`dry_stub.py:97`).
- (a) The walker translates §3.3 into the built control. Cost: a translator, and two meanings of `repair_on_round` (mapping vs
  int) living side by side. Error direction: a translation loss is silent.
- (b) Amend §3.3 to the built grammar; the walker passes `stub` through `merge_stub` and lifts `conductor` (item 4). Cost: one
  Lead amendment of P1-b §3.3 (it is a spec edit that changes a meaning, so PROJECT.md package change п. 6 asks a critic on the plan).
  Error direction: none new; the stub already refuses a mistyped key (`dry_stub.py:651-653`).
- (c) Change the stub to §3.3. Cost: rewrite `dry_stub.py` and `story.json`, re-run the main pass; outside this node's owns.
- Recommendation: **(b)**. One grammar for the story, the type row (R3 §5 item 1) and the walk row (P31).

**F-W2. Row id namespace (coordinator point (a)).**
- (a) Keys stay bare (`s1.review/go on`); other subjects carry `route:`, `joint:`, `kind:` (`route:s1_gap/code move`,
  `kind:s1_gap/free words`, `joint:exit_gate:grounding/word`). Cost: `_walk_problems` resolves the namespace; `driven_keys` is
  unchanged; known_red ids change form for non-key rows (none exist today, `known_red.json:3-5`).
- (b) A precedence rule (key > kind > route > joint). Error direction: the wrong one: a route row is silently judged as a kind row.
- (c) An explicit `subject: {"section": ...}` field. Cost: two places for one fact (the id and the field).
- (d) Merge a route and the kind it raises into one subject. This decides a census question (the two are separate entries today,
  P1-b §3.2), so it is not for this node.
- Recommendation: **(a)**. Error direction: an un-namespaced non-key id is refused, never guessed (EW8).

**F-W3. Variants of a joint, and `*` joints (point (b)).** §3.3 lists variants for keys, keyless kinds with words, and code routes;
it is silent for joints.
- (a) Joint variants `repair` (the row's `repair_on_round` repairs: C3 expected), `no repair` (C5 expected), `word` (the person's
  word passes: C4 expected, gate class). A `*` joint is one subject: any refusal of that detector family that the walker observes
  (F-W4) satisfies it.
- (b) One variant per concrete refusal tag of the family. Cost: an open set the census cannot list.
- (c) Joints are not walked as rows; C1 (the census) is enough. Cost: the `gate` class (43 joints, P1-b `:345`) loses C4g.
- Recommendation: **(a)**. Error direction: the variant set is closed and small; a family with an unobservable tag stays
  `live_only` with its reason.

**F-W4. How a route or joint firing is observed.**
- (a) A passing spy in `dry_driver.py` on the module function `driver_machine.match_known`, writing `state/dry-routes.jsonl`
  (the F10 (a) technique); joints by the refusal text naming the check, via the driver's own first-refusal line (`first_refusal`,
  `dry_world.py:454-457`) plus `class_of`. Cost: `dry_driver.py` joins the owns; a producer and its reader in one commit (AR-22).
  Risk: a caller that bound `match_known` by name before the patch would bypass the spy, so the spy is installed before
  `story_run` is imported, as the price spy is (`dry_driver.py:55-58`).
- (b) Apply `driver_machine.match_known` in the walker to the refusal text it sees. Cost: no new producer. Error direction: text
  derived, so it can name a route the driver did not take.
- (c) Route and joint rows `live_only` until a later node.
- Recommendation: **(a)** for routes. For joints, (a)'s refusal-text road is unverified: the builder measures, on the first
  joint row of the self-test or of N4:s1-s4, whether the exit gate's refusal line names the check id, and reports it. If it does
  not, joint rows are `live_only` with that reason. Error direction: a joint never counts as observed by a guess.

**F-W5. Where the snapshots of an exits part come from** (`main_pass` destroys its own, `dry_world.py:1007-1008`; it takes 381 s,
N2g `:43`).
- (a) Each part builds its world and runs a main-pass PREFIX up to its latest `start` (item 1 `stop_after`), with the same road as
  the main pass. Cost: s0 and s1-s4 pay about the first turn; gates pays to S4 (most of the 381 s); s5 and s6-s9 pay to the S4
  stop today. Parallel CI parts stay possible.
- (b) One process: main pass, then every group's rows. Cost: one long job (no parallel parts); a red in one group hides nothing,
  but the job is long.
- (c) Snapshots carried between CI jobs as artifacts. This breaks P1-b §4.3 "lives only in this run" and E16's process label.
- Recommendation: **(a)**. Error direction: none for correctness (same road, same labels); the cost is CI time, which F6 / N5 caps.

**F-W6. Snapshot timing: turn end vs stage border; states before S0 closes.** Today `S<n>` = "stage n closed, taken at the end
of the turn that closed it", so S0 is at the `s1_review` question and S1..S3 are at `gate_A`. States inside S0 (group s0: `halt`,
`package`, `ticket_changed`, routes `no_project`, `uninitialized`, `s0_receipt`, ...) come BEFORE any snapshot.
- (a) Keep the timing, print the snapshot index (each snapshot: last closed stage, pending question kind, stage statuses) so N4
  builders pick the latest snapshot BEFORE their state and reach it with `drive_until` and the row's stub. Add `start: "fresh"` =
  the world exactly as `build_story_world` makes it (real writers, no driver run) for pre-S0 states. States that need a different
  WORLD (no project config, an uninitialised project) are not reachable by any seed under §4.3's prohibitions: the N4:s0 part marks
  them `live_only` with that reason.
- (b) Drive the main road in single-boundary steps (`--max-boundaries 1`; a boundary is one loop turn, `driver_machine.py:1909`)
  so a snapshot is taken at the border. Cost: unmeasured, many more processes; the main pass's own time grows. Measure first
  (CLAUDE.md hygiene 6a).
- (c) A world-variant field in the row (`world: {"config": ...}`). It widens §4.3 (config is written by the walker); it is a
  new grammar element for the Lead.
- Recommendation: **(a)** now, with `fresh` added to the `start` vocabulary (one more snapshot name, made by `walk_exits` before the
  first driver turn); (b) as a measurement queued for N5; (c) not now. Error direction: a row started too late cannot reach its
  state, and the seed reports "did not reach" (EW17), never a pass.

**F-W7. What C2 means operationally** (P1-b `:78` "each offered variant has an executor"; §3.4 `:302-306` "at least one variant
other than `stop` changes the fingerprint").
- (a) Per row: the answered token was offered, the driver recorded the answer for that ask, and no `unread_answer` conductor call
  followed. Per subject (group level): "alive only stop" (item 9).
- (b) C2 = C3 (the fingerprint changed). Cost: no separate meaning; a taken answer that legitimately changes nothing is red.
- (c) Data only: each offered option maps to a price row with a non-empty `factory` executor. This duplicates K15's data side.
- Recommendation: **(a)**. Error direction: a token the driver refuses as "not one of the answers" (the `unread` path,
  `driver_machine.py:3316-3321`) is red, never green.

**F-W8. The expectation of the `empty` variant.** P1-b E9: an empty file -> the expected `Stop` "is empty", not a skip. No check id
names it.
- (a) A check `empty`: the answer turn printed the driver's empty-answer refusal, and the same ask is still pending.
- (b) No rows for `empty` until a later node. Then §3.3's variant list stays partly unwalked (it counts in `unwalked`, item 10).
- Recommendation: **(a)**. Error direction: an empty answer silently taken as an answer is red.

**F-W9. What `unwalked` counts per group, and whether it is red.** No per-group figure exists today (`dry_exits.py:565-573`).
- (a) The census `unwalked` entries of the group + the group's walk subjects missing a demanded variant (item 10). Price keys with
  no row anywhere stay with the existing census (P1-b `:233-234`). A NOTE, not red: the census ratchet (AR-20) holds the count.
- (b) Also count price keys "of the group". There is no data that says which group a key belongs to (only the prose list
  P1-b `:636`); that would need a new table.
- (c) Red when > 0. The `dry-story` job would be red until every group is complete.
- Recommendation: **(a)**. Error direction: a missing variant is printed with its id; the N4 DoD asks 0.

**F-W10. Static `after:` in a row vs the dynamic `after:`.** P1-b `:636` says the s5 and s6-s9 rows are `after:FV1-1` today; E15
says they run by themselves after the fix.
- (a) A row that waits only for a snapshot carries `reach: seed|story` and its natural `start`; the walker prints the dynamic
  NOTE `after:<node>` while the snapshot is missing (EW11). A static `after:<id>` is kept for a row that waits on a defect OTHER
  than a missing snapshot: not run, NOTE, counted in the census ratchet `after`.
- (b) Rows carry static `after:` and the walker still runs them when the snapshot exists. A green run then leaves a stale reach
  that someone must edit, which the fix node does not own.
- Recommendation: **(a)**. Error direction: never PASS while unreachable; no stale reach after the fix.

**F-W11. The shape of `seeds/<group>.json`.** N4 owns the file (P1-b `:628`), but no grammar is given anywhere; a row's `seed` is
inline in §3.3 (`:255`).
- (a) Named recipes (section 8); a row's `seed` is a recipe id or null. One form; the variants of one subject share a recipe.
- (b) Seeds inline only; drop the file from N4's owns.
- (c) Both. Two roads (P31).
- Recommendation: **(a)**.

**F-W12. Rows for owner questions Q1 and Q2 (E10, E22).** The grammar has no field for them.
- (a) `expect.owner_question: "Q<n>"`: the row is not run and prints NOTE `owner question Q<n> open`; after the owner's answer,
  the Lead replaces it with `owner_quote` (E22).
- (b) `reach: live_only` with why "owner question Q1 open". It mixes a reach reason with an intent question, and the census counts
  it in `live_only`.
- Recommendation: **(a)**.

**F-W13. Checks not built here: C7, C8 (the expectation), C9, C10.** They are assigned to exit rows (§9.3, E9, E14).
- (a) Build C9 here (pure data, reachable at S2 on today's main: FV1-6); C7, C8-expectation and C10 go to a follow-up node; a row
  listing them prints NOTE `pending judge` and is not reconciled (EW26).
- (b) Build all four here. Cost: C10 cannot be proved before P1B-9 is fixed (S5); C7 needs a definition of "reached whole" over
  three carriers (P1-b AR-24 row), which is a design question of its own.
- (c) Build none; a row listing them is refused. Then the FV1-6 rows cannot be written.
- Recommendation: **(a)**, with a queue line (Q-1). Error direction: no row is green on an unjudged check.

**F-W14. `start: after:<id>` in §3.3 (`:254`).** Its meaning is not defined beside `reach: after:<id>`.
- (a) Drop it from `start`; `reach` carries `after:` (F-W10).
- (b) Keep it as "a snapshot that exists after finding <id> is fixed". No such snapshot is ever made under §4.3.
- Recommendation: **(a)**.

**F-W15. Variants of keyless kinds whose options are dynamic (`conductor`, point (c)).**
- (a) Variant = `<why>:<token>` (`kind:conductor/stage_review_exhausted:rework_stage`), plus `free words` and `empty` for kinds
  whose question carries words (`conductor`, `refusal`, P1-b `:245-246`). The `<why>` is one of the seam's closed `why` values
  (P1-b `:164`); the token must be offered by the stub's control at that ask.
- (b) Variant = the token only. Two different states of the conductor collapse into one id.
- Recommendation: **(a)**.

**F-W16. Where E15's "never expected red for the defect that made it unreachable" lives.** `known_red.py` has no such rule
(read whole).
- (a) In the walker's `judge_group` (item 9). The walker is the only place that knows the dynamic `after:` of a row.
- (b) In `known_red.py` (P1-a's helper). It would need the `after:` labels passed in: a new argument for every consumer.
- Recommendation: **(a)**. A queue line tells P1-a (Q-2).

**F-W17. The per-row cap (E6: "the Lead assigns after N0").** Today `ROW_CAP = 60` (`dry_world.py:43`), and N0's probe rows ran
with `ROW_CAP * 4` per process (`:497`, `:509`).
- (a) 240 s per row (seed + answer + post turns), with a FAIL beyond it (EW23); the part's own cap is N5's.
- (b) No per-row cap; only the job cap. A slow row then shows only as a slow job.
- Recommendation: **(a)**, the value to be confirmed by the Lead after the self-test's measured seconds.

**F-W18. The local run of `--part main` after the refactor (DoD 6, ~381 s).**
- (a) Run it once on the final state (the N2g precedent). Cost: about 6.5 min of one builder run, beyond the minute rule.
- (b) The canon judges it (`full` job); locally only the pure-table row of `drive_main`. Risk: a refactor break of the main pass
  shows only at the canon.
- Recommendation: **(a)**, because item 1 moves the main pass's own loop.

Questions for the owner: none. Every fork above is a design or interpretation question inside an accepted plan; no requirement of
the owner is itself unclear.

---

## 12. Small choices I closed (no design weight)

- S-1. The executor (data collection, driver processes) goes in `dry_world.py`; the judgment (pure) goes in `dry_exits.py`. No new
  file (TESTING.md `:117`; P1-b §10 names the four helper files).
- S-2. Reserved variant names in English: `free words`, `empty`, `code move`, `words:<case>`. `free words` is the form the built
  selftest already uses (`dry_exits.py:1574`).
- S-3. `POST_TURNS = 4` single-boundary turns after the answer: C5 needs a third ask, plus one turn of slack.
- S-4. Closed `op` script list: `story_step.py`, `stage_done.py`, `waiver.py`, `controller.py` (P1-b §4.3 `:448-449` names these
  four). A data tuple in `dry_exits.py`.
- S-5. CLI options `--exits-root` and `--ledger` instead of a reserved group name for the self-test (one road: the self-test is
  just another root).
- S-6. `why_unreached` on a runnable row is refused (one meaning per field).
- S-7. Answer file bytes: `token + "\n" + words`. **Estimate, not verified** against the driver's reader of a token plus words;
  the self-test proves token-only; N4's E9 rows prove the combined form or report it.
- S-8. A row's main-pass prefix lines are printed as NOTE `exits:<g>/prefix: ...`, never PASS/FAIL (no main verdict twice in
  the canon).

## 13. Queue lines (noticed, not widened)

- Q-1. A follow-up node for C7 (words reached whole: brief, `state/words/`, conductor call) and C10 (FV1-19 two readers), with a
  definition of "reached" for C7 written by the designer; C8's expectation once the owner answers (F9, E22).
- Q-2. P1-a / `known_red.py`: E15's rule lives in the walker (F-W16 (a)); if the P1-a walk needs it too, a shared form follows AR-15.
- Q-3. `slow_tests.json:119` `51.0` and `selftest.py:117` `900` vs N2g's measured 381.2 s for `--part main` (N2g `:43`): the
  N3-era figure is stale; the owner of N3 item 7 rows (N3 / Lead) updates it. The ceiling (900) still holds.
- Q-4. TESTING.md `:124-125` ("one world per file; a subprocess per check is a defect of the test") vs P1-b §4.3 (a driver process
  per row on a snapshot copy). The spec decided it; the text of TESTING.md does not name the dry story's exception. Tie it to F2
  (the TESTING.md edit waiting for the owner, P1-b `:757-760`).
- Q-5. `dry_driver.py:13-14` names E17 as "the walker's" check; this node writes it. Nothing to queue once N4w lands; listed so the
  critic sees the producer/reader pair close.
- Q-6. P1-b §3.3 needs the Lead's amendment after F-W1, F-W2, F-W3, F-W11, F-W12, F-W14, F-W15 (one edit). PROJECT.md package change
  п. 6 (b): a spec edit that changes a meaning gets a critic pass on the plan.
- Q-7. The N4 card's group list (P1-b `:636`) mixes price keys, kinds and why-states (point (c)): reword it when the Lead amends §3.3.

## 9b. Sibling axes (rule 10 (b): every axis; the axes this node leaves as P1-b §7(b) left them are cited there)

- axis 1: n/a, no deployment or role rule changes.
- axis 2: n/a, no tier exams.
- axis 3: covered, files under `scripts/tests/` ship as package tests; the release fingerprint covers them.
- axis 4: queued, FR debt unchanged; Q-1..Q-7.
- **axis 5 (stage twins)**: covered. One executor for every stage's rows; groups are data. The C4 rule is by class, not by stage;
  the s5 and s6-s9 groups go through the same code as s0 (they print `after:` today by data, not by a branch).
- axes 6, 7: n/a, measurers and test identity unchanged; the scoreboard stays P1-v's (§3.5 call reused).
- axis 8: covered, copies and snapshots live in temp dirs; no machine path is written into a fixture (`words_file` is relative and
  confined, EW14).
- axes 9, 10, 11: n/a.
- axis 12: covered, the node sits in P1-b's pile/batch by the Lead.
- axes 13-16: n/a.
- **axis 17 (one output shape)**: covered. The walker prints only `scenario_walk.Result` kinds through `harness.check` and `NOTE`
  lines, with the main pass's names (`dry-1/<part>/<id>`) and its known_red forms (`dry_world.py:956-962`). No second form.
- **axis 18 (shrink-only ratchets)**: covered. No base changes in this node; the `unwalked` per-group figure is a NOTE (F-W9 (a)),
  and the census ratchet stays the only ratchet. The self-test ledger is a separate file and has no pin (it is not a ratchet: it
  is read only by `--ledger`; `dry_exits.check()` never reads it, I14).
- axes 19-29: n/a (no host, no markdown tables read, no `tests[]` row fields).
- axis 30: n/a, the automator's commands are untouched (the stub's, N2).
- axis 31: n/a.
- axis 32: covered, section 1's owner/class table.
- axis 33: n/a.
- **axis 34 (one road)**: covered. The rows use the same driver process, the same `drive_main` road and the same closed-words
  source as the main pass; `story` and `seed` reaches run identically; the self-test group uses the same loader as N4's files
  (only the root differs); language is not a parameter here (the runner row is the kit's, F5). The one asymmetry, s0 states that
  need a different world (F-W6), is returned as a fork with the one-road option (c) priced, not written as "not supported".
- axes 35, 36: n/a.

Four questions (rule 10) for the mechanism this node adds (the walker's checks): (a) cost: one sequential builder node and CI time
per part (F-W5); every future exit row is a JSON row; (b) above; (c) detector: the walker IS the detector of AR-25/AR-28 for exit
rows, and its own failure (a row silently skipped) is caught by the `outcomes` check (I1) and the census (I8, `_walk_problems`);
external: calibration check per P1-b R-L4 (not yet written: a finding already listed in P1-b `:713-715`); (d) on the path: job
`dry-story` (N5) runs every part; `--witness-for` names the dry story for any edit of the helper files.

## 14. Reading trail

| What | Where | Result |
|---|---|---|
| P1-b | `BR\docs\tasks\specs\20261113-p1b-dry-story-spec.md` 1-899 | §1 checks `:75-87`; §3.2 `:173-237`; §3.3 `:239-267`; §3.4 `:269-306`; §3.5 `:308-316`; §3.6 `:318-371`; §4.3 `:440-453`; §4.4 `:455-470`; E1-E22 `:476-499`; N0-N-L `:522-677`; §10 `:847-861` |
| R3 | `BR\docs\tasks\specs\20261113-p1b-n0-round3-amendment-spec.md` whole | `stub` grammar of a type row (§5 item 1), E-R3 form, E-R8 |
| The part | `T\test_scenario_dry_1.py` 1-75 | `parse_part :44-50`, `main :53-70` |
| World, main pass | `T\dry_world.py` 1-1023 | as section 2 |
| Census | `T\dry_exits.py` 1-962 read; 963-1658 by Grep of `def`/`@case` plus 1550-1658 read | as section 2; `free words` variant `:1574` |
| Stub | `T\dry_stub.py` 1-142, 398-417, 600-659, 729-908; Grep of `def`/constants | control grammar, conductor, journal, run class |
| Wrapper | `T\dry_driver.py` 1-64 | price spy; E17 named as the walker's `:13-14` |
| Ledger helper | `T\known_red.py` 1-153 | `reconcile :130-152`; no `after` rule |
| Walker | `T\scenario_walk.py` 36-115, 880-937; Grep | `DOORS :40` holds `driver`; `Result :66-70`; `witness_for :888-923` |
| Harness | `T\harness.py` Grep | `check :115-118`, `finish :225-229` |
| Fixtures | `T\fixtures\driver-exits\known_red.json`, `s0.json`, `s1-s4.json`; `T\fixtures\stories\dry-1\story.json` | as sections 2 and 10 |
| Schedule rows | Grep `dry_1\|dry_exits\|dry-1` over `test-layers.json`, `slow_tests.json`, `selftest.py` | keep row `:5101-5115`; `slow_tests.json:119` 51.0; `selftest.py:117` 900 |
| References | Grep `stage-joints.json` (`"check": "<x>:\*"`) and `question-prices.json` (keys) | `*` joints `:398,475,501,547`; `s3.grounding_*` keys `:250-262`; `s1.review :107` |
| Driver | `driver_machine.py:1900-1929`, `:3310-3349`; Grep `max.boundaries` | a boundary is one loop turn (`:1909`); default 80 (`story_run.py:159`) |
| Controller | `controller.py:2398-2453` (Grep) | `passed-by-person.jsonl` fields `stage, dispatch, block, decision, by` |
| Reports | S0R whole; S14R whole; N2g `:7`, `:25-64` | the main pass to S5, 381.2 s, snapshots S0..S4 |
| Rules | TESTING.md Grep (`:117`, `:124-125`); builder-rules `:14-34` | as cited |
| Sibling map | `docs\SIBLING_MAP.md` Grep of axis headings | axes 5 `:111`, 17 `:373`, 18 `:386`, 34 `:582` |

Negative claims, each with a positive control of the same shape:
- "No walker code: `key not observed`, `drive_until`, `owner_quote`, `exits:` appear in no `.py` under `T`": Grep `-i`, glob `*.py`,
  path `T`, pattern `key not observed|drive_until|owner_quote|"exits:|'exits:` -> no match. Control: the same call with
  `|run class not propagated` in the alternation found `dry_stub.py:613`. (The words "key not observed" in `dry_driver.py:13-14`
  are split across two lines, which is why a single-line search misses them; a direct Read shows them.)
- "`fixtures/stories/dry-1/` holds no `exits/` or `seeds/`": Grep `.` files_with_matches over that folder lists 7 files
  (`story.json`, `kit.json`, `impl.diff`, `ticket\DRY-1.md`, `runners\python-pytest\...` x3). That listing is itself the control
  (it lists the existing files). A Glob on the `.claude\worktrees` path returned nothing (the Glob limit R3 `:309-311` also met), so
  Glob was not used as evidence.
- "`known_red.py` has no `after` rule": read whole (`:1-153`), a direct read, not a search.
- "No per-group `unwalked` figure": `_count_reach` and `_ratchets` read whole (`dry_exits.py:565-573`, `:669-688`); the only other
  `unwalked` sites are vocabulary and selftest rows (Grep of `def` lines and the read of `:1-962`).
- "`World.control` never writes a top-level `conductor`": direct read `dry_world.py:266-270`.

Not read: `form_filler.py`; `driver_dialog.py` (the answer-record field names are cited from P1-b `:119-121`; the builder reads
`driver-answers.jsonl` once to confirm `question_sha`); the whole of `stage-joints.json` (only the `*` lines and one entry
`:385-414`); the remote `origin/wip/p1b-*` branches (S0R `:18` reports that search; not repeated here).
