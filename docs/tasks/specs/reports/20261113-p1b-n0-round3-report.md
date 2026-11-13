# P1-b node N0, round 3 - builder report

Branch `wip/p1b-n0`; code commit `9cf28f5` (on `066011d`); this report is the next commit. Type `codemie-14857`.
Outcome in one line: the relevance verdict of TP1-15791 is now declared data (`relevant`, the recorded run's verdict) and the stub carries it through
`peek`, `assess` and the complete collection; S1 STILL does not close, because the collected ticket TP1-15791 names further mentioned tickets
(TP1-10937 first) that the type does not declare. The road ends at that labelled `live_only` (the cascade the spec predicted, F-R3-3), the gate line
is `undecided`. S2 and S3 are not driven on CI. The stop is NOT the relevance of TP1-15791 (DoD 5 satisfied).

## What was done (items of section 5)
1. `dry-types.json`: type `codemie-14857` gains `stub.source_relevance."TP1-15791" = {relevance: relevant, reason: "explicit required source",
   from: "investigation-14857/TP1-14857/work/source-inventory.json:432-433"}` (value and reason verified at `source-inventory.json:432-433`). `dry_world.check_stub`
   (called from `load_types`): `stub` absent = `{}`; not a mapping, `source_relevance` not a mapping, value outside `relevant|not_relevant|unknown`, empty/blank reason,
   case-folded duplicate key: `TypesError` naming file, type and key (E-R3).
2. `dry_world.merge_stub` + `World.control`: control = type `stub` overlaid by the row's `stub`, row wins key by key (one level below the top: role, ticket key); the main pass has the type's stub alone.
3. `dry_stub.judge_sources` (pure over a `runner`), wired into `fill_role` for S1 scout calls: for each required source with `relevance: pending` whose key is in `source_relevance`:
   `ticket_adapter.py peek <KEY> --output <inv>`, reload, then `assess --output --source-id --relevance <v> --reason <r> --assessment-ref <the ref peek wrote>`.
   Key not named: no command, `live_only` naming the source (the round-2 text). Failure of any command: `live_only` with its text cut at 400, never retried with another value.
4. Cascade: a source the stub itself judged `relevant` (status still `pending`, `source_inventory.py:3220`) gets `collect <KEY> --relation referenced --output <inv> --summary`
   (s1.md "Source collection", lines 146-157: the complete collector, a read; it is the one step added). Further mentions that collect brings in are judged the same way if declared, else `live_only`.
   A kept source left pending with no read step is named by `pending_judgments`. `inspect --inspection-status` (a judgment) is NOT run: J5 untried (not reached).
   Bounded: 8 rounds of the loop.
5. `pending_judgments` reads through `source_inventory.load_inventory` (`read_sources`); no write of `source-inventory.json` anywhere in the stub (grep below).
6. `form-fill-rules.json` (F-R3-4 a): `work/requirements-register.md` template gains `## Branches` / `Branches: none -- <why>` and `## Source obligations` with header `| unit | home |` and one row
   `| rest | unreconciled: <why> |`; `required` gains the two `body:` headings. No `## Attachments` row (the S2 refusal was never reached, so nothing asked for it). Grounding (J16) untouched: not reached, no generator yields a hunk path (non-goal: no new generator).
   `test_field_producers.py`: one new row (register carries both sections with the contract's empty form, header and `rest` row).
7. `dry_world.gate_line`: numbers verdict only when `statuses()["S3"] == "done"`, else `gate: undecided -- the road ended at <stage>: <first 160 chars of its outcome line>; measured: S0..<stage> <s> s, row median <s> s`.
8. `dry_world.tree_hash` / `snapshot_red`: the snapshot of each row `start` is hashed before the rows and after each row; a change is `red: snapshot changed by a row: <row id>` and the spike exits 1. CI: no red.
9. `probe.json`: row `halt/words` gains `"s1_review": "go on"`; nothing else changed.
Also (E-R2): `dry_world.unused_judgments` prints `NOTE: unused judgment <key>` for a declared key the main pass never judged.

## Witness
```
$ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/tests/dry_stub.py scripts/tests/dry_world.py
no scenario or keep row covers scripts/tests/dry_stub.py: run the whole scenario layer
scripts/tests/dry_stub.py: test_scenario_cart_1.py  (and local_1_0108, local_1_arm_b, walk, world)
no scenario or keep row covers scripts/tests/dry_world.py: run the whole scenario layer
scripts/tests/dry_world.py: test_scenario_cart_1.py  (same five files)
```
(as expected by the spec: no row covers these files; the five files it names are big scenario files, not run here.)
```
$ (package dir) python -B scripts/tests/dry_stub.py --selftest | tail -1
=== dry_stub --selftest: 57/57 ok ===          (round 2: 33/33; 24 new rows: named key argv, E-R1 no command, E-R4 refusal, E-R5 no ref, kept-pending, E-R10 cut, E-R2 note, item-2 overlay x2, E-R3 x7, item 1, AR-28 gate x3, E-R8 x2)
$ (package dir) python -B scripts/tests/test_field_producers.py | grep "known red rows\|==="
known red rows 29, not in world rows 47, rows walked 910
=== test_field_producers: 921/921 ok ===          (round 2: 920/920, known red 29, not in world 47, rows walked 909: counts unchanged)
$ (package dir) python -B scripts/selftest.py --lang
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===
$ grep -nEi "write_text|write_bytes" scripts/tests/dry_stub.py     (AR-14 check)
  only: the stub journal (line 209), the handover form (243), selftest fixtures; no `source-inventory` write. `pending_judgments` -> `read_sources` -> `source_inventory.load_inventory`.
$ grep -niE "codemie|14857" scripts/tests/dry_stub.py scripts/tests/dry_world.py   (AR-1 check)
  hits only in the selftest (tracker routes of the type under test, `["codemie-14857"]` expected id list); none in the road or the stub code; positive control: `codemie-14857` is in dry-types.json:1.
```
CI run `43500065530` (`gh workflow run canon.yml --ref wip/p1b-n0 -f ref=wip/p1b-n0 -f spike=true`), job `dry-story-spike` 132143250422 success (`start`, `clock` success, `full`/`checks` skipped). Read with
`python -B tools/ci_read.py jobs 43500065530` and `python -B tools/ci_read.py log 132143250422 --grep ''` (time prefix cut; CI log shows some characters as `?`):
```
NOTE: gap mybooks-local-1: live_only - no raw tracker input for LOCAL-1 (waits ?L F-A1-6)
NOTE: gap no-autotests: owner question OQ1 open - no type without automated tests (waits OQ1)
world built in 0.0 s
S0 driver exit 0 in 3.8 s? work/ticket-snapshot.json key = 'TP1-14857'
turn 0: driver exit 3 in 6.8 s? question s1_review? stages {'S0': 'done', 'S1': 'running', 'S2': 'absent', 'S3': 'absent'}
turn 1: driver exit 4 in 1.2 s? question conductor? stages {'S0': 'done', 'S1': 'running', 'S2': 'absent', 'S3': 'absent'}
S1..S3 8.0 s in 2 driver process(es); seconds per stage {'start': 4.5, 'S1': 3.5}; stop: the road met the conductor: a state the driver has no move for (stub journal and first refusal name it)
outcome S0: done
outcome S1: running - live_only: work/source-inventory.json: 1 mentioned source(s) await the scout's judgment (http://127.0.0.1:44603/browse/TP1-10937): `ticket_adapter.py peek` then `assess --relevance` is role judgment and the type holds no closed answer for it; first refusal: review --record failed (exit 3): ticket_adapter: review rejected: assess these sources before showing the review: SRC-9fbf2b62c70cd679f31e
outcome S2: not reached - after an earlier stage that did not close
outcome S3: not reached - after an earlier stage that did not close
row s1.review/go on: 8.0 s - asked s1_review (as expected); answered; next turn exit 4
row questions/answers: 8.2 s - asked s1_review (as expected); answered; next turn exit 4
row halt/words: 6.8 s - live_only: expected a halt question, the road meets s1_review first (stub journal: [... "ran": ["peek TP1-15791 exit 0", "assess TP1-15791 relevant exit 0", "collect TP1-15791 referenced exit 0"], "judged": ["TP1-15791"] ...])
tracker: 15 requests, 4 distinct, 2 without a route (404): ['/rest/api/2/field', '/rest/api/2/issue/TP1-14857/remotelink']
spike[codemie-14857]: S0..S3 11.8 s; snapshot 0.0 s; row median 8.0 s; rows 3
gate: undecided -- the road ended at S1: running - live_only: work/source-inventory.json: 1 mentioned source(s) await the scout's judgment (http://127.0.0.1:44603/browse/TP1-10937): `ticket_adapter.py ; measured: S0..S1 11.8 s, row median 8.0 s
```
No `red:` line (snapshot guard clean), no `NOTE: unused judgment` (TP1-15791 was judged), no `UNLABELLED RED`.

## Seconds table (CI, one run)
| what | seconds |
|---|---|
| S0 (driver process, REST) | 3.8 |
| S1 turn 0 (to the question `s1_review`; driver start counted in "start" 4.5) | 6.8 |
| S1 turn 1 (after "go on", to the conductor) | 1.2 |
| S2, S3 | not reached |
| S0..S3 as printed | 11.8 (this is S0 + S1 only) |
| snapshot (byte copy of the S0 world) | 0.0 |
| rows `s1.review/go on` / `questions/answers` / `halt/words` | 8.0 / 8.2 / 6.8 (median 8.0) |

## Outcome per stage
- S0 done.
- S1 not closed. New this round: `peek` + `assess relevant` + complete `collect` of TP1-15791 all exit 0 (journal `ran`), the stage-1 refusal for TP1-15791 is gone.
  The stop is the NEXT source: collecting TP1-15791 adds the tickets it names as `pending` mentions (TP1-10937 first), and the type declares no value for them -> `live_only` naming TP1-10937 (E-R1), the review refuses, the driver asks the conductor.
- S2, S3: not reached on CI.

## Local probe (not committed, not a witness; Windows is several times slower)
To see the next stop I ran the spike locally ONCE with a temporary dry-types.json that also declared the other six tickets of the recorded run
(`source-inventory.json`: TP1-10937 relevant; TP1-12034, TP1-12780, TP1-13171, TP1-13289, TP1-217 not_relevant), with placeholder reasons; the file was restored from a byte copy (sha256 `e46f6067...5a24` before and after) and
the committed file declares TP1-15791 only. Result: S1 goes further: all six judged, TP1-10937 (relevant) collected, `s1_review` answered, then the driver asked `s1_gap` (`vcs_evidence could not collect <MR 4566>: cli_missing`; TP1-15791's merge request is media the
factory cannot reach in the dry world). No probe row names `s1_gap`, so the road stops there (A1-E3: `question 's1_gap' has no answer in the probe rows`). S2/S3 still unreached. Local probe numbers (S0..S1 82 s) are not comparable to CI.

## Stops, with labels
1. (committed state, CI) S1: `live_only` - mentioned ticket TP1-10937 (a cascade of TP1-15791) has no declared value.
2. (local probe only) S1: question `s1_gap` (MR of TP1-15791 unreachable: `vcs_evidence` `cli_missing`) has no answer in the probe rows - a person-side closed answer, A1-E3.
3. Beyond those: S2 and S3 untried. J10 (units' homes) now has the contract's remainder form in the template; J11 (attachments), J16 (grounding hunk path `diff:src/app.py:1` vs the world's 25-file diff) untried.

## Templates / fields added (derivation lines)
| added | derived from |
|---|---|
| type row field `stub.source_relevance` (value `relevant`, reason `explicit required source`) | recorded run `investigation-14857/TP1-14857/work/source-inventory.json:432-433`; F-R3-3 |
| register template `## Branches` / `Branches: none -- <why>` | `references/artifact-contract-plan.md:19-20` (empty form); `branch_accounting.py:517-539` (refuses `none --` with no reason) |
| register template `## Source obligations`, header `| unit | home |`, row `\| rest \| unreconciled: <why> \|` | `artifact-contract-plan.md:21-23`; `branch_accounting.py:57-58` (`OBLIGATION_COLUMNS`), `:603` (`unreconciled:` prefix), `:692,704-707` (`rest` takes `unreconciled:` only) |
| step `collect <KEY> --relation referenced` after a declared `relevant` | `skills/qa-story/phases/s1.md:146-163`; `source_inventory.py:3220` |

## Deviations and facts that differ from the spec (reality)
1. Spec item 4 names "the complete collector" only generically; it is `collect <KEY> --relation referenced` (s1.md:163 says it refuses a ticket not assessed `relevant`, which is exactly the order the stub follows).
2. The spec predicted the cascade as `inspect`; the actual first cascade is NEW MENTIONS brought by the collector of the kept ticket (TP1-10937 etc.), a class the spec's J-table did not list (J4 repeated for each discovered ticket).
3. `--witness-for` prints the five scenario files for both paths, which the spec said it would ("run the whole scenario layer"); nothing was run for it.
4. The stop `s1_gap` (local probe) is a person-side question; the spec's J6 flagged it as "untried".

## Analogs noticed (not fixed)
- Every ticket the recorded run judged has a recorded value in the same `source-inventory.json` (7 more rows); declaring them is the same move as item 1 but a new decision (F-R3-3 names one ticket only): returned as Question 1.
- `form-rounds.json` / `form_filler.py` / `known_red.py` etc. are also unregistered in `plans/features.json` (pre-commit WARN door (d), 10 offenders now; 3 of mine: `dry_stub.py`, `dry_world.py`, `probe.json`, plus `form-fill-rules.json`) - R2 Q2, left with the Lead (S-5).
- Round 1/2 note stands: `FakeJira` (`test_story_run_s0.py`) and `TrackerServer` are one server (clone candidate).

## Questions
1. The road ends because TP1-15791's collection brings in six more mentioned tickets the type declares nothing for. The recorded run holds a verdict for each (list above, same carrier). Declare all of them in `stub.source_relevance` (same grammar, `from` = the recorded line)? The local probe shows S1 then runs to `s1_gap`.
2. After that the road meets `s1_gap` (the MR of TP1-15791 is unreachable in the dry world: `vcs_evidence` `cli_missing`). A closed answer exists only if a probe row names `s1_gap` (A1-E3); which words (accept the gap?) is the person's word, so I did not add one. Needed for any road past S1.
3. Per the "no round 4" rule: whatever the Lead decides on 1-2 belongs to N2 or a Lead-owned amendment, not to this node.

## Needed beyond the manifest
`skills/qa-story/phases/s1.md`, `scripts/branch_accounting.py` (lines 437-470, 594-607), `scripts/source_inventory.py` (peek_jira_source 1819-1893, update_inventory), `ticket_adapter.py` (peek/assess handlers 2738-2790), the recorded `source-inventory.json` whole (verdicts of all tickets), `tools/ci_read.py`, `scripts/tests/test_field_producers.py` (rows near 960-1000).
