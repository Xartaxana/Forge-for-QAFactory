# P1-b node N0, round 2 - builder report

Branch `wip/p1b-n0`; code commit `35b1899` (on top of round 1's `7dca70c`); this report is the next commit. Type `codemie-14857`.
Outcome in one line: the filler now writes `work/impl-diff.txt` and the manifest's `source_sha`, S1 runs to its source review (the question
`s1_review` is reached and answered), and the road then stops at ONE labelled `live_only`: the relevance judgment of a mentioned ticket
(`ticket_adapter.py assess`), which no writer or contract of the world can state. S2 and S3 are therefore NOT driven; S0..S3 below is
still a lower bound. Question 1 asks the Lead how to close that gap.

## What was done
1. Filler kind `work/impl-diff.txt` (was a `not_covered` row): `form-fill-rules.json` `artifact_templates["work/impl-diff.txt"]`
   (format text, template `<the diff text>`), artifact token `<the diff text>` -> `FillContext.impl_diff` (new field, empty = unfillable,
   naming the token, nothing written). Derived from: `references/artifact-writers.json` (writer `qa-scout (the role)`, "written once from the MR
   or branch the person named"), contract line `references/artifact-contract.md:23` (the line naming the file, used as the template's
   `anchor`), and the readers' own shape (`context_bundle.bounded_diff`, `diff_pass.py`: a unified diff). The value is the world's own raw
   VCS answer: `fixtures/stories/dry-codemie-14857/tracker/mr-4566.diff` (byte copy of the K5 corpus file, `cmp` identical, 105,995 bytes),
   registered as a route row `serves: mr_diff` in `tracker/routes.json`; read by the new `dry_world.mr_diff(row)` (bytes decoded, no
   line-ending change). `not_covered` lost its `work/impl-diff.txt` row.
2. Template field `implementations[0].source_sha` of `work/context-manifest.json`: value `0000000000000000000000000000000000000000`, marked
   by the new row key `synthetic` ("declared synthetic ... no repository exists in the dry world"). Derived from: `context_bundle.py:22`
   (`SOURCE_FIELD_HINTS`: the commit the diff was read at), `context_bundle.py:71-73` (required key of each `implementations[i]`),
   `references/record-schemas.json:244-258` (ContextBundle `source_revisions[].source_sha`, required, non-empty), and the zero value
   precedent `references/profile-shape.json:30`. The stub journals the mark (`synthetic` list on its row), so the value is never passed as a fact.
3. Stub: `ROLE_STEPS` (the scout's `ticket_adapter.py collect <KEY> --relation task --output work/source-inventory.json`, s1.md "Source
   collection": a read by the tracker client, decides nothing); `pending_judgments()` turns a required source with `relevance: pending`
   into a `live_only` row with its reason (E13); the filler context gets `impl_diff` from `dry_world.mr_diff`.
4. World/road: class `Road` answers the real driver's questions ONLY with `closed_answers(rows)` (the words a probe row names; A1-E3), turn by
   turn (one driver process per turn), snapshots each stage that closes, ends at gate A, at a kind no row answers, or at the conductor
   (a state the driver has no move for); `stage_outcomes` names the stuck stage, `live_only` and the first refusal line verbatim (`first_refusal`).
5. Bug of my round 1, fixed: `dry_world._rewrite` rewrote absolute paths inside `state/events.jsonl`, breaking its hash chain
   (`story_step: refused - corrupt event 2; writes blocked`), so every probe row's copy of the snapshot hit the conductor before any role ran.
   Now `events.jsonl` is skipped by the rewrite. This is why rows 1 and 2 now reach their named question.
6. `probe.json`: row 1 lost its `result_text` guess (the default result text reaches `s1_review`); row 2 gained `"s1_review": "go on"` in `answers`
   (the first question of its road is now `s1_review`; the word is the one row 1 names).
7. `test_field_producers.py`: `WORLD_DIFF` constant, `impl_diff=` in the output-walk context, three new rows (diff lands byte for byte; no diff
   in context -> unfillable naming the token and `write_outputs` writes nothing; `source_sha` is a 40-hex commit id and the row marks it synthetic).
8. `dry_stub.py --selftest`: 26 -> 33 rows (E13 row rewritten: impl-diff and manifest are `fill`; mr diff bytes; no-diff unfillable; pending
   judgments three cases + missing file; `closed_answers`).

## Witness
```
$ python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest | tail -3
PASS gate: the numbers of the spec
=== dry_stub --selftest: 33/33 ok ===
$ (package dir) python -B scripts/tests/test_field_producers.py | grep "known red rows\|==="
known red rows 29, not in world rows 47, rows walked 909
=== test_field_producers: 920/920 ok ===          (before this round: 915/915, known red 29, not in world 47, rows walked 904)
$ (package dir) python -B scripts/selftest.py --lang
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===
```
Ledger (`form-rounds.json`), summary-line form: before `readers 19, families 3, not_in_world 47, known red 29` -> after the same. No row removed, no
row added, no pin changed: the new kinds turn no `not_in_world` row green (the round world writes no `impl-diff.txt`; `derive: ...implementation.diff.*`
rows still say "none in the world" for the ROUND world, which is a different world from the dry world).

CI run `43493681799` (`gh workflow run canon.yml --ref wip/p1b-n0 -f ref=wip/p1b-n0 -f spike=true`; executes the branch's copy), job
`dry-story-spike` 132121139140 success; `checks`/`full` skipped, `clock` success. Read: `python -B tools/ci_read.py jobs 43493681799` and
`python -B tools/ci_read.py log 132121139140 --grep ''` (time prefix cut; the CI log shows some characters as `?`):
```
NOTE: gap mybooks-local-1: live_only - no raw tracker input for LOCAL-1 (waits §L F-A1-6)
NOTE: gap no-autotests: owner question OQ1 open - no type without automated tests (waits OQ1)
world built in 0.1 s
S0 driver exit 0 in 4.2 s; work/ticket-snapshot.json key = 'TP1-14857'
turn 0: driver exit 3 in 5.9 s; question s1_review; stages {'S0': 'done', 'S1': 'running', 'S2': 'absent', 'S3': 'absent'}
turn 1: driver exit 4 in 1.4 s; question conductor; stages {'S0': 'done', 'S1': 'running', 'S2': 'absent', 'S3': 'absent'}
S1..S3 7.3 s in 2 driver process(es); seconds per stage {'start': 5.0, 'S1': 2.3}; stop: the road met the conductor: a state the driver has no move for
outcome S0: done
outcome S1: running - live_only: work/source-inventory.json: 1 mentioned source(s) await the scout's judgment (.../browse/TP1-15791): `ticket_adapter.py peek` then `assess --relevance` is role judgment and the type holds no closed answer for it; first refusal: review --record failed (exit 3): ticket_adapter: review rejected: assess these sources before showing the review: SRC-50693ee590c6eac703d3
outcome S2: not reached - after an earlier stage that did not close
outcome S3: not reached - after an earlier stage that did not close
row s1.review/go on: 7.3 s - asked s1_review (as expected); answered; next turn exit 4
row questions/answers: 7.2 s - asked s1_review (as expected); answered; next turn exit 4
row halt/words: 5.9 s - live_only: expected a halt question, the road meets s1_review first (...)
tracker: 7 requests, 3 distinct, 2 without a route (404): ['/rest/api/2/field', '/rest/api/2/issue/TP1-14857/remotelink']
spike[codemie-14857]: S0..S3 11.5 s; snapshot 0.0 s; row median 7.2 s; rows 3
gate: continue (S0..S3 11.5 s, row median 7.2 s, worst row 7.3 s)
```

## Seconds table (CI, one run)
| what | seconds |
|---|---|
| S0 (driver process, REST) | 4.2 |
| S1 (turn 0 to the question `s1_review`; driver start 5.0 s counted in "start") | 5.9 (turn 0) |
| S1 after the answer (turn 1, to the conductor) | 1.4 |
| S2, S3 | not reached |
| S0..S3 total as printed | 11.5 |
| snapshot (byte copy of the S0 world) | 0.0 |
| probe rows `s1.review/go on` / `questions/answers` / `halt/words` | 7.3 / 7.2 / 5.9 (median 7.2) |

Local (my machine, label `local`, three runs while building; Windows is several times slower than CI): S0..S3 47-53 s, rows 7-32 s. Not a witness.
I ran the spike locally while developing (a deterministic script run of about a minute, `dry_world.py --spike --label local`, the form the
spike itself provides); the DoD asked for CI as the witness, which is above.

## Outcome per stage
- S0 done.
- S1 not closed. Cleared this round: `impl-diff.txt` written, `context-manifest.json` accepted (exit gate "witness OK"), `context-bundle.json` built
  by `context_bundle.py` (no more `source_sha: missing`), handover form filled with `implementation.diff.files=25 hunks=29 production_files=14` by code,
  the person's source review asked (`s1_review`) and answered "go on". Stops at `ticket_adapter.py review --record`: "assess these sources before
  showing the review" - the one mentioned ticket TP1-15791 is `relevance: pending`; judging it (`peek`, `assess --relevance relevant|not_relevant|unknown
  --reason ...`) is the role's judgment, and nothing in the type (A1: raw tracker/VCS answers, `words: {}`) names a closed answer. Label: `live_only`,
  not red, not hand-written (E13). The driver then asks the conductor (`stub: the prompt lists no open move to offer`), where the main pass ends.
- S2, S3: not reached.

## Probe rows
- `s1.review/go on`: driven from the S0 snapshot, reaches `s1_review`, answered, next driver turn exit 4 (the same refusal as the main pass).
- `questions/answers`: reaches `s1_review` (expected `any`), answered with the words of row 1; next turn exit 4.
- `halt/words`: `live_only`, blocked by stage S1: the scout's source review and judgments speak before any halt (driver_dispatch.py:725-728 position
  invariant B-1, the scout's `s1_person` runs inside `handoff`), so a `halt` question cannot be reached while S1 does not close.

## Gate verdict by the numbers (reported, not acted on)
By the spec's numbers: `continue` (11.5 s <= 120, row median 7.2 s <= 20, worst row 7.3 s <= 60). CAUTION, same as round 1: the road still ends inside
S1, so 11.5 s is the cost of S0 plus S1 up to the review, not of S0..S3; S2 and S3 (the strategist's forms, the plan files, the gate A question) were
not driven. The rows now start from a real S1 state, which is progress, but two of three end at the same blocker. Weigh the verdict on that.

## Filler kinds / template fields added (the derivation lines)
| added | derived from |
|---|---|
| `work/impl-diff.txt` kind, token `<the diff text>` | artifact-writers.json (writer), artifact-contract.md:23 (anchor line), context_bundle.bounded_diff / diff_pass.py (shape) |
| `implementations[0].source_sha` (synthetic zero id) | context_bundle.py:22, :71-73; record-schemas.json:244-258; profile-shape.json:30 |
| `FillContext.impl_diff`, `dry_world.mr_diff`, route row `serves: mr_diff` | A1 table row "Ответы трекера/VCS ... `*.diff`: кладутся в `dry-<type>/tracker/`" |
Kept `live_only` (no writer or contract defines a value for the dry world): the relevance verdict of a mentioned ticket; `work/reference-snapshot.yaml`
(code writer `reference_snapshot.py`, S-c stories only, out of the main pass); the later stages' role outputs are untried (not reached).

## Deviations and facts that differ from the spec (reality)
1. The snapshot copy corrupted the event hash chain (item 5): spec 4.3 says a row starts from a COPY of the snapshot; a copy with paths rewritten inside
   `events.jsonl` is refused by `story_step` (`corrupt event 2`). Round 1's rows never reached their state for this reason too, not only because of S1.
2. The S1 first dispatch is two stops in the driver, not one: after the scout's digest the driver asks `s1_review` (which needs every mentioned source
   assessed), and only after "go on" runs a second scout session. The N0 spec's S0..S3 picture has no source judgment in it; the world holds one
   mentioned ticket (TP1-15791) that the task's description names.
3. `tracker: 7 requests` in the world (was 3): `collect` reads the task again; same 3 distinct paths, same 2 without a route (404).
4. `dry-types.json` untouched (the diff is not in the table: `kit` is not fed to the run, A1 line 102).

## Analogs noticed (not fixed)
- The `events.jsonl` hash chain and `_rewrite`: any other chained file in a world copy (none seen; `controller.json` known_paths rewrite works).
- Round 1's note stands: `FakeJira` of `test_story_run_s0.py` and `TrackerServer` are the same server (clone ratchet candidate).
- `form-rounds.json` `not_in_world` rows "needs a diff under work/" describe the ROUND world of test_field_producers; the dry world now has a diff but the
  registry rows are judged on the round world, so none went stale. A round that reads the dry world would turn three of them green (a later node).

## Questions
1. S1 cannot close without the relevance verdict of TP1-15791 (and S2, S3 cannot be driven). Recommendation: the type row names it as data
   (`words`/a new `assess` map, e.g. `{"TP1-15791": "not_relevant"}`, with the reason words), and the stub runs `ticket_adapter.py peek` + `assess` with
   exactly that, and refuses (live_only) for a source the row does not name. That is a design decision on what the world may state as the person's/role's
   judgment (A1-E3 spirit), so I did not implement it. Alternative: accept N0's measure as it stands and judge the gate on S0 + S1-to-review.
2. Register the new package files in `plans/features.json` (pre-commit door (d); WARN lists 10 offenders, 3 of mine: `dry_stub.py`, `dry_world.py`,
   `probe.json`)? Not in my owns.

## Needed beyond the manifest
`driver_dispatch.py`, `driver_machine.py`, `source_preflight.py`, `source_inventory.py` (statuses), `skills/qa-story/phases/s1.md`, `agents/qa-scout.md`,
`references/stages.json`, `references/artifact-writers.json`, `references/record-schemas.json`, `references/profile-shape.json`, `story_step.py`
(refusal text), `tools/ci_read.py`; not in the given basket: `test_workflows`-style files were not needed.
