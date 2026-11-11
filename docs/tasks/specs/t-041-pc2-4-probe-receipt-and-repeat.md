# t-041 / PC2-4 — the walk writes its receipt once; a repeat is answered only by a whole record

Batch `package-ci/2`, node PC2-4. Owner's word 11.11.2026: «Да, в работу». Intent brief: `plans/piles/package-ci/findings/20261111-kanon-krasnyj-probe-by-code-povtor-obhoda-i-raspiska.md`.
Status: DRAFT (designer, t-041) — three forks at the end need the Lead before dispatch (F1 and F3 change test expectations/fixtures the brief asked to keep).

All paths below are under `C:\QAFactory\forge-repo\ai-packages\qa-factory\` unless absolute. `PBC` = `scripts/probe_by_code.py`, `PL` = `scripts/proof_level.py`, `T` = `scripts/tests/test_probe_by_code.py`.

## 1. What changes, AR-n touched, owner and census class of every check

Three causes keep six checks of `T` red (journal t-035 witness: `756/762 ok`):

| red check (`T`) | line | cause (traced in code, §2-§4) |
|---|---|---|
| «pinned invert: its notes» | :2327 | the walk attaches the receipt on two publishes of one walk; the second gets the note `... already holds this proof` (§3) |
| «pinned invert: the written record's key set» | :2325 | the aggregate carries `judgment_owed` and `walk_ended`, absent from `INVERT_RECORD_KEYS` :2303-2312 (§4) |
| «pinned answer: exit 0, the walk answers with the aggregate again» | :2335 | stale pin: the repeat of a complete walk is `already_probed` by deliberate decision B3 (§2, fork F1) |
| «pinned answer: the key set is the aggregate's» | :2337 | same as above (F1) |
| «a corrupt record: the check is not proved, so the probe runs again» | :2510 | the receipt answers the repeat before anything reads the corrupt per-check records (§2, fork F2) |
| «an incomplete record does not answer a repeat: the probe runs» | :2521 | NOT `already_probed` (the finding is wrong here): the walk CARRIES the survivor from its per-check record (F3 amendment); the fixture stamps only the aggregate (§2, fork F3) |

AR-n touched (change check of each is in the DoD, §6):
- **AR-14** (one artifact, one writer): `_aggregate_record` stays the one writer of `work/probes/<iid>.json` (:6770-6771) and `write_receipt` the one writer of a receipt (:4057); only the NUMBER of receipt-attaching calls per walk changes (2 -> 1).
- **AR-22** (every field produced has a reader): `judgment_owed` and `walk_ended` keep their producer and are named with readers (§4); no field is removed.
- **AR-13** (one reader): the per-check record is read only through `_read_check_record` (:6033-6041, "the ONE reader of `work/probes/checks/`").
- **AR-28** (an unknown never becomes a pass): the repeat answer gains one more "unknown -> walk" branch (F2); the gate row `test_identity` in `references/gate-registry.json` lists `already_probed` with `unknown_branch: "rerun"` (:117-129).
- **AR-29**: no judgment moves into code. Checks this node adds or alters:

| check | owner | census class | note |
|---|---|---|---|
| receipt attached once per walk (`_walk_plan` publish order, §3) | data | — (not a check unit: an order of writes) | |
| `_repeat_same_entries` (PBC :7281-7305) gains "each proved row's per-check record reads and agrees" (F2, recommended option) | data | shape (presence, readability, equality of two stored keys) | not a refusal: a False sends the call to the walk; no census row expected (`_repeat_same_entries` has none today; `_repeat_check` has one, `judgment-census.json` :614) |
| `T` pins edited (`INVERT_RECORD_KEYS`; F1, F3 fixtures/expectations) | data | — (tests) | |

## 2. Which change made a repeat `already_probed`, and which side is intended

Evidence:
- **B3 (t-2064 fix round A) is the deliberate decision**: `_probe_plan` asks the repeat question before `_entries_for` (PBC :7416 comment "fix round A, B3: the old road's one question") and answers `already_probed` for a complete aggregate on the same bytes and entries (:7420-7421, via `_repeat_same_entries` :7281-7305 and `_repeat_answer` :7308-7314). Spec `docs/tasks/specs/t-2064-probe-every-check.md:541` item 4: "all proved and the aggregate standing: `already_probed` as today". Pinned green by `tests/test_probe_fix_round.py:172-193` (`test_b3_repeat_of_a_complete_walk_is_already_probed`), and by `T` :1361-1365 (TR2-14 B3) and :2384-2399.
- **F3 (Lead, §14 amended 11.11.2026) is the second deliberate decision**: a per-check `no_failure` / `wrong_location` record on the same entry, bytes key and flags is CARRIED, not run (spec t-2064 :824; PBC :6030 `_CARRIED_VERDICTS`, :6450-6452). Pinned by `test_probe_fix_round.py:196-208` and `T` :2454-2459.
- The pins at `T` :2332-2337 predate B3 (their comment asks "is `already_probed` kept for the walk's repeat?" — B3 answered yes). The pins at `T` :2502-2504 and :2514-2516 predate B3/F3 (they speak of "the walk reads no note", "`already_probed` is unchanged").

Per case:
- **Whole record** (receipt on the row, aggregate `intended_failure`, every proved per-check record readable): answers `already_probed` — the Lead's direction = B3. The two «pinned answer» checks expect the opposite and must be repinned (fork F1).
- **Corrupt per-check records, receipt and aggregate intact** (`T` :2505-2508): today `already_probed(...)` hits item 1 (receipt, PL :1448-1478), `_repeat_is_new` is True (the receipt carries `checks`, PBC :4017-4023, :7278), `_repeat_same_entries` compares only the receipt's rows (:7289-7304) -> answered, 1 launch; the pin wants 2. The Lead's direction (corrupt -> run, FR-59) needs a new condition (fork F2).
- **Stamped `incomplete` aggregate, per-check record `no_failure`** (`T` :2517-2522): `already_probed` item 2 reads the aggregate (PL :1483-1491), sees `incomplete`, no hit; target is None at `_repeat_look` (:7249-7250) so no per-check path is read -> `{"probed": False}` -> walk -> `_check_standing` (:6072-6086) reads the per-check `no_failure` -> carried (:6450-6452) -> 1 launch, verdict `no_failure`. The pin wants 2. The cause is F3 + a fixture that stamps a record the walk no longer reads (fork F3). Not verified by a run (designer has no shell): the builder's first step records the actual values (§6 step 0).

## 3. One receipt write per walk

Where it happens today: `_walk_plan`'s local `publish()` (PBC :6404-6412) calls `_aggregate_record` every time; `_aggregate_record` calls `attach_receipt` whenever `verdict == "intended_failure" and not unfinished and restore verified` (:6910-6913). `publish()` runs after every group (:6530) AND once more at the end (:6549). After the LAST group of a complete walk both calls see a complete plan -> `write_receipt` runs twice with the same `receipt_hash` (the hash excludes `evidence_refs`, :4050-4054) -> the second finds the file and returns the note `<rel> already holds this proof` (:4067-4076), appended to that record's notes by `attach_receipt` (:4139-4141).

Change (closed small choice, see §8): in the loop, publish only when the walk CONTINUES to another group. Replace :6529-6532

```
        write(group, index < len(groups) - 1 and not result["ended"])
        publish()
        if result["ended"]:
            break
```
by: `write(...)` as is; then `if result["ended"]: break`; then `if index < len(groups) - 1: publish()`. The end-of-walk `publish()` at :6549 and the no-group `publish()` at :6457 stay. Update the comment at :6530 to say: intermediate aggregates after every row but the last; the last row's aggregate is the final one at :6549.

Why this is enough: an intermediate publish has groups not yet run, whose rows are `not_reached`, so the plan is not complete and `attach_receipt` is never reached there (EP-K, :6910-6912). So every walk path reaches the receipt-capable call exactly once: :6457 (no group to run) or :6549 (after the loop). `write_receipt` itself is NOT changed (its note is right for a file that predates the walk).

INVARIANT kept: within one walk `write_receipt` is called at most once, so the note «already holds this proof» appears only when the receipt file existed BEFORE this walk — a rerun of the probe (a person's word, `T` :1366-1379; a walk with every check proved whose row lost the receipt ref, :6457) still gets it; one walk never does. The aggregate on disk never claims more than the per-check records (it may lag by one row, never lead).

## 4. `judgment_owed` and `walk_ended`: readers (AR-22)

- `judgment_owed` — producer `_judgment_fold` (PBC :6751-6752, "always written"), merged at :6897. Readers: `PL.probe_record_state` (PL :1121-1126, returns it) -> `PL.probe_plain_call_owed` (PL :1165-1176, `got["judgment_owed"] == []`), which the window's note and `probe_word_door` read (docstring PL :1168-1169). Also pinned by `test_probe_every_check.py:2386-2425`, `test_probe_judge_languages.py:49`, `test_probe_product_publish.py:211-235`.
- `walk_ended` — producer `_aggregate_record` (PBC :6890). Reader: `_refold` (PBC :7795, `"ended": str(agg.get("walk_ended") or "")`), the judge's rebuild of the aggregate, which `_aggregate_verdict` reads through `walk["ended"]` (:6798-6800).
- Search trail: Grep `judgment_owed|walk_ended` over `ai-packages/qa-factory/**/*.py` (positive control: the same search found both producers, PBC :6752 and :6890).

Both have readers -> both go into `INVERT_RECORD_KEYS` (`T` :2303-2312), which is compared with `sorted(written)` (:2325), so keep it sorted: `"judgment_owed"` between `"instance_identity"` and `"manifest_fields_missing"`; `"walk_ended"` between `"verdict"` and `"window_probe"`. Nothing is removed from the record. Update the comment at :2300-2302 with one clause naming the two keys and their readers.

## 5. Edges, each with its invariant

| # | edge | behaviour | invariant protected |
|---|---|---|---|
| E1 | empty walk plan | `_probe_plan` refuses before any lock or write (PBC :7408-7409, `_empty_plan_refusal`); `_aggregate_record` writes nothing for no checks (:6792-6795). No publish, no receipt. Unchanged. | an empty list is never read as all proved (EP-A) |
| E2 | every check already proved (no group to run) | one publish at :6457; the receipt is written, or found with the note «already holds» when the file predates this call. Unchanged. | the note means "this file was there before this walk" |
| E3 | walk interrupted between publishes (killed, time, restore failed, stop) | an intermediate aggregate is never complete -> never a receipt. Killed after the last row's per-check records and before :6549: the aggregate on disk is the previous row's (or absent for a one-group walk), no receipt from this walk; the next call finds no receipt, walks, every check proved -> :6457 writes the receipt. An ended walk (`ended` set) now breaks without the in-loop publish and gets exactly the :6549 one. | a receipt exists only for a complete walk with a verified restore (EP-K, :6910-6912); the aggregate never leads the per-check records |
| E4 | a receipt file from an earlier story | unreachable: receipts live under the story's own `task_root/work/sensitivity-receipts` (:3998, :4063). From an earlier walk of THIS story with the same facts: same name, note «already holds» (legit rerun). Same name, other content: nothing written, `receipt: None`, note "already exists with different content" (:4072-4075). Unchanged. | a receipt measured on other bytes never counts; an immutable receipt is never overwritten |
| E5 | the corrupt-record detector of F2 is wrong | it may err ONLY toward False (walk again): an absent, unreadable, non-object per-check record, one whose `verdict` is not `intended_failure`, one whose `entry_sha` differs from the receipt row's -> False. Adversarial inputs that must stay on the walk side: `{not json`; `[]`; `{}`; a dict with `verdict: incomplete` / `no_failure`; a dict with another `entry_sha`; a missing file; an `OSError` on read (all already map to None or a mismatch through `_read_check_record`, :6037-6041). Rows whose receipt verdict is `not_owed` have no per-check record (they never run, :6380-6381) and are not read. | a corrupt or unknown record never answers `already_probed` (FR-59, AR-28); the cost of an error is one extra run, never a false "already probed" |
| E6 | the row names a receipt whose file is gone | `already_probed` reads no receipt -> no hit -> walk (PL :1449-1453). Unchanged. | as E5 |
| E7 | a person's recorded word on a repeat | `_repeat_look` returns no answer, the walk reruns proved checks (:7244-7247); its one receipt-capable publish (:6549) finds the earlier file -> note «already holds» (`T` :1378). | as §3 |

## 6. The builder node

```
given: C:\QAFactory\forge-repo\docs\tasks\specs\t-041-pc2-4-probe-receipt-and-repeat.md (this spec, whole); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\probe_by_code.py (:4057-4142, :6404-6550, :6742-6917, :7240-7314, :7384-7421, :6033-6086); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\proof_level.py (:1095-1176, :1404-1532); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py (:2286-2350, :2353-2523); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_fix_round.py (:139-208); C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md (whole); C:\QAFactory\forge-repo\plans\builder-rules.md (whole); C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\probe_by_code.py (functions `_walk_plan`, `_repeat_same_entries` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py (functions `the_record_and_the_answer_are_pinned`, `the_repeat_is_answered`, the list `INVERT_RECORD_KEYS` and its comment only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\package-ci-2-probe-receipt-and-repeat.md
non-goals: `write_receipt` / `attach_receipt` / `_aggregate_record` bodies; `proof_level.py`; B3 and F3 behaviour (a whole record stays `already_probed`, a survivor stays carried); any other red check of the canon (PC2-5..PC2-7); a new test file or a new test function; the quarantine section of test-layers.json; selftest/install_smoke.
handoff: the builder report (`.claude/agents/builder.md` rule 7) with the FR pass, the witness verbatim, the six checks named with their before/after lines, and the commit hash on `pile/package-ci/batch-2`
edges: E1-E7 of §5 of this spec
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py` all ok; plus `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_fix_round.py`, `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py` and the files `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <owns>` prints
```

Steps:
0. Run `T` once before any edit; copy the six FAIL lines with their actual values into the report. If an actual value differs from the trace in §1/§2 (in particular «an incomplete record ...» is expected to show `('no_failure', 1)`), STOP and return the line as a question.
1. §3 — the publish order in `_walk_plan`.
2. §4 — add the two keys to `INVERT_RECORD_KEYS`, sorted.
3. Forks as accepted by the Lead (recommended options below): F1 repin of the two «pinned answer» checks; F2 the extra condition in `_repeat_same_entries`; F3 the fixture of the «incomplete» group.
4. Changelog fragment (English): the walk writes its live receipt once; a repeat whose per-check records cannot be read runs the probe again.

F2 (recommended) in code: inside `_repeat_same_entries`, after the existing per-row comparison (:7300-7304), for each `(check, row)` whose `row["verdict"] == "intended_failure"`: `stored = _read_check_record(ctx.task_root, _records_id(ctx), check["line"], _ordinal_of(check), check.get("file"))`; return False unless `isinstance(stored, dict) and stored.get("verdict") == "intended_failure" and stored.get("entry_sha") == row.get("entry_sha")`. Extend the docstring: "a proved row whose per-check record is absent, unreadable or disagrees with the receipt is not a repeat: the call walks (FR-59, error direction: walk)". Bytes are not re-compared here: `already_probed` item 1 already holds the receipt over these bytes (PL :1448-1478).

Acceptance keys:
- K1 the six checks of §1 are `ok`. Their expectations are UNCHANGED except: `INVERT_RECORD_KEYS` (§4), and whatever the Lead accepts in F1 and F3 (named, line by line, in the report).
- K2 no other check of `T`, `test_probe_fix_round.py`, `test_probe_one_road.py` turns red (compare the before/after FAIL lists of step 0 and the final run).
- K3 tests per `docs/TESTING.md`: no new test function, no pin of source text, no pin of a measured constant; F3's fixture is an edit of the existing group; a case added for E5 (if any) is a row of an existing parameterised check, not a new function.
- K4 AR change checks: AR-22 — the grep of §4 repeated with its positive control, quoted in the report; AR-13 — the new read goes through `_read_check_record`, no `json.loads` of `work/probes/checks/` added; AR-28 — `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_registry.py --check` green (if it names `_repeat_same_entries`, STOP and return: adding a site row to `references/gate-registry.json` is outside `owns`); AR-29 — `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` green with no row change (same STOP rule for `judgment-census.json`).
- K5 the commit message carries `architecture: AR-13, AR-14, AR-22, AR-28 -- <how kept>` and `judgment: data -- <one line>`; `selftest.py --lang` green (English only).

## 7. Forks (the Lead decides)

**F1 — the two «pinned answer» checks (`T` :2335, :2337) contradict B3.**
- (a) RECOMMENDED: repin them to the B3 answer — `(proc.returncode, answer.get("verdict")) == (0, "already_probed")` and `sorted(answer) == sorted(ANSWER_KEYS + ["notes"])` (the keys of `_repeat_answer`, PBC :7311-7314); rewrite the comment :2332-2334 to say B3 answers the walk's repeat. Cost: two expectations change, against the brief's "unchanged" key; this is the Lead's own direction (whole record -> `already_probed`).
- (b) keep the pins: the walk must answer a complete repeat with the aggregate — that reverts B3 and turns red `test_probe_fix_round.py:172-193`, `T` :1361-1365 and :2384-2403. Not recommended.

**F2 — corrupt per-check records under an intact receipt (`T` :2510).**
- (a) RECOMMENDED: `_repeat_same_entries` also requires every proved row's per-check record to read and agree (§6, F2 in code). The pin stays as written. Matches the Lead's direction and FR-59; cost: one small file read per check on every repeat, and one extra run when a per-check record is damaged. A heavier variant (answer only when the walk would launch nothing, i.e. `_check_standing` for every check with the walk's bytes keys) needs the bytes-key computation of :6432-6444 factored out of `_walk_plan`; not needed for the pin, not recommended now.
- (b) the receipt stands alone (it is the immutable proof over these bytes): repin :2510-2512 to `already_probed` with 1 launch. Cost: an expectation changes; a damaged walk record goes unnoticed until the bytes change.

**F3 — the «incomplete» group (`T` :2517-2522) stamps a record the walk no longer reads.**
- (a) RECOMMENDED: keep the expectation `("no_failure", 2)` and fix the fixture: stamp `verdict: "incomplete"` also on the per-check record(s) (`task_of(root)/work/probes/checks/test_dead_assert--*.json`, the same glob shape as the corrupt group :2506-2508); rewrite the comment :2514-2516 to name F3 ("a stored `incomplete` per-check record reruns; a survivor is carried"). Then `_check_standing` returns `incomplete`, not in `_CARRIED_VERDICTS`, and the check runs — F3's own words (spec t-2064 :824). Cost: a fixture edit in an existing check, against the brief's "unchanged"; no code change.
- (b) the walk also reads the aggregate's verdict and reruns every survivor when it says `incomplete` — a second source of standing beside `_check_standing` (AR-13) and against F3. Not recommended.
- (c) change the expectation to `("no_failure", 1)` — drops B-373's meaning on the walk road. Not recommended.

### Answers to the forks (Lead, 12.11.2026)

- F1 — (a): the two «pinned answer» checks are repinned to the B3 answer. B3 is a decision in force with its own green pins; the two checks predate it.
- F2 — (a): a proved row whose per-check record is absent, unreadable or disagrees is not a repeat; the call walks (FR-59).
- F3 — (a): the expectation `("no_failure", 2)` stays, the fixture stamps the per-check record too.
- The handoff line of §6 is read without the branch: the batch works in the shared tree on `main`, the builder does not commit; the Lead commits.

## 8. Small choices closed by the designer

- Place of the one-write fix: the publish order in `_walk_plan` (§3), not an in-process "written by me" set threaded through `_aggregate_record` -> `attach_receipt` -> `write_receipt` (more plumbing through three signatures, same effect) and not a `final` flag on `publish()` (the in-loop call after the last group is simply redundant with :6549).
- `write_receipt`'s note text and its immutability rule are untouched.
- No new census or gate-registry row is planned; K4 makes the gates say so.

## 9. Reading trail

Finding (whole). PBC :3985-4160 (receipt core, `_hash_of`, `write_receipt`, `attach_receipt`), :4696-4712 (single-road attach), :5950-6120 (`_attempt_why`, `_check_record`, `_check_proved`, `_CARRIED_VERDICTS`, `_read_check_record`, `_same_bytes`, `_check_standing`), :6380-6570 (`_walk_plan`), :6735-6917 (`_judgment_fold`, `_aggregate_record`), :7230-7430 (`_repeat_look` ... `_probe_plan`), :7780-7851 (`_refold`, `judge_record`). PL :1095-1176, :1404-1532. `T` :1340-1389, :2270-2552. `test_probe_fix_round.py` :139-208. Spec t-2064 :489-541 (grep), :815-826. `design/architecture.md` :148-174, :232-281. `references/gate-registry.json` :115-139. `scripts/tests/fixtures/judgment-census.json` :1-5, :609-614. `scripts/tests/test-layers.json` :2695-2799 (all three witness files are keep rows: data_join). `plans/builder-rules.md` :14-26, :77. Journal `logs/journal/dev1.jsonl` :80 (t-035 witness: no actual values recorded — hence step 0). Greps: `judgment_owed|walk_ended` (package .py, positive control = producers found); `already holds|already_probed|corrupt|not json|walk_ended|judgment_owed` over the two sibling test files (only B3/one-road pins; none reads the two keys or corrupts per-check records).

Needed beyond the manifest: `proof_level.py`, spec `t-2064-probe-every-check.md`, `gate-registry.json`, `judgment-census.json`, `test-layers.json`, the journal line of t-035.
