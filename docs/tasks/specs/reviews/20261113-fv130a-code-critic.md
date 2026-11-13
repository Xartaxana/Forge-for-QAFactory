# Code critic — t-499, node FV1-30a (diff 5c16666..a4fc87b, worktree fv130a)

**Verdict: NEEDS WORK (fit_with_fixes) — 2 blocking findings, 6 to fix in this round, 9 minor or to queue.** I give a verdict only. Accepting the work is the Lead's decision.

Spec: `docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` §A3, items 1–4 (lines 330–373) and edges A3-E1..E6.

## Blocking

**B1. `_names` checks whole-identifier containment the wrong way, so a word passes findings it never named (K2; spec item 3, the forbidden direction).**
`s5_precheck.py:3950` calls `C.names_whole(word, tag)`. That returns True when the TAG contains the WORD as a whole identifier (`contract.py:134`: needle = word, text = tag). Any sub-identifier of a tag that sits after a character outside `[\w-]` (`[`, `=`, `.`, `:`) therefore names the finding. Probe results (trail P1/P2):
- The word `missing-assistant` (a partition label) passed `run_mapping:TC-1:no-row-test_validate_per_partition[missing-assistant]`, `manifest:TC-1:dup-…` and `bindings:TC-2:ghost-…`. That is three findings across two cases, and the word is neither a tag nor an id.
- `id` names `contradicted-literal-1-body.id`. `12` names `changed-after-red-a.py:12`. `neg` names `no-row-…[neg]`.

This is the t-108 class again, at the instance level: every finding whose tag ends in the iid (`no-row`, `unmatched`, `dup`, `shape`, `ghost`, `red-own-*`) passes on the instance's parameter label. The spec's parenthesis `names_whole(match, tag)` has the same inversion, but its prose ("names its tag WHOLE") and its own error-direction rule forbid this outcome.
The opposite effect follows too: the spec row "a 24 KB word naming the tag passes" can never hold, because a long `match` is never contained in a short tag. The test only pins a 24 KB `decision`.
- **Smallest fix:** `s5_precheck.py:3950`: replace `C.names_whole(word, tag)` with `low == tag.lower()`. Equality errs toward a false refusal, which is allowed. The other direction, `names_whole(tag, word)`, would let a sibling's whole id (`bindings:TC-2:no-bindings`) pass `no-bindings` of TC-3.
- **Test row** in `one_road_selects_the_word_for_the_finding`: a parametrised iid with the word = its parameter label passes nothing. The current row "a part of a tag does not name it" uses only hyphen-bounded parts (`bindings`, `row`, `no`), so it cannot catch this defect.

**B2. Three test files in the CI canon's keep list are left red, so the batch canon would fail (K3; `docs/TESTING.md` «Когда тест покраснел» p.1: a test that turns red because behaviour changed on purpose is rewritten in the same node).**
`test_s5_precheck_sides.py` S10, `test_then_remainder.py` K3 and `test_stand_gap_remedy.py` are in `keep` (they run in canon). `test_row_fields.py` and `test_s5_precheck_plan.py` are in `quarantine` (test-layers.json; trail P4). The node cannot be accepted with three red keep files.
- **Fix:** the Lead widens `owns` by these three files. The fix round re-pins them as in the K3 table below.

## Fix in this round

**F1. The printed door no longer works (K2; FR-2, FR-37, FR-57, AR-9).** `report` (`s5_precheck.py:4727-4736`) still prints `--block "<part of the line>"` plus `WHOLE_PART` "(whole words of the line)". It also says the word "passes an [environment] or [obligations] finding or a changed-after-red/… one; no recorded word, `*` included, passes any other finding here - it is a repair."
After 30a both statements are false:
- a phrase of the line passes nothing. The builder's own row 21 in `test_words_doors` pins that the printed-line word passes nothing.
- every family is passable, so the text tells the orchestrator not to ask the person about the findings 30a has just made passable.

Smallest fix inside 30a is item 6 (1) brought forward: the door becomes `--block "<the finding's tag, or its whole id>"` passes that finding. Add one clause that `*` passes every finding here except `open-oracle-asserted-*` (answer the expectation question) and a Then left with its owner (the existing sentence stays). `awaits_answer` and `detector_verdict` stay in 30b. Drop `PASSABLE` from the text.
This **blocks a separate merge**: if 30a and 30b converge on one batch branch before `main`, F1 can ride with 30b.

**F2. `word_passes` is not pure, and it runs the whole check up to three times (FR-45, FR-55; K6/K9).** `word_passes` → `run()` → `passed_by_judge` (`s5_precheck.py:4651`) → `judge.judged_refusal`, which asks the judge and writes the judge journal (`judge.py:373-388`) when `judge.mode` is on or shadow. One accepted completion calls it from:
- `_record_s5_word_passes`,
- `_s5_no_row_passed`,
- `branch_accounting._word_passed_ids` (from the exit gate).

The purity test passes only because the judge provider is `none`.
Fix: take the passes before the judges. Either `run(..., judges=False)`, or split out a collection step that ends at `_judge_words`. In `word_passes`, return `[]` early when `C.live_stage_overrides(pipeline, ("S5",))` is empty.

**F3. The finding id is parsed in three new places (AR-13; brief item 6).**
- `controller.py:7365`, `branch_accounting.py:1929` and `s5_precheck.py:4045` each split `finding_id` with `split(":", 2)`.
- The existing reader `s5_precheck._finding_tag` is at `:4098`. `exit_gate._finding_tag_of` is at `:1775`.

Fix: the `_judge_words` pass row carries `check`, `case` and `tag` taken from the finding dict, and the three readers read those fields.

**F4. `_plan_refusal` records a pass inside `validate` (K6).** `controller.py:6505` runs during `validate("dispatch")`, which means:
- it also runs in the story_step probe on a COPY of the state (`story_step.py:2329`, "a refusal there costs nothing"),
- it runs on requests that a later check refuses,
- it writes again for every window request while the word stands.

The record shape is the same (one writer, same keys; `dispatch: ""` is a value, not a second shape, so AR-18 holds), but this writes for probes and refused requests. The spec does not ask for it.
Fix: drop it from 30a and queue it, or record it after the commit (`_after_commit`).

**F5. Docstrings and comments that now contradict the code (brief item 7, "names that lie").** They still say "outside PASSABLE / no word passes / `*` included" at `s5_precheck.py`:
- `:80-88`, `:95-98`, `:1520`, `:2372`, `:3812-3813`,
- `:3961-3963` (`refusal_cause`: "every other then-remainder-* … keeps the family line"),
- `:4556`, `:4616`, `:4633`, `:4725-4726`.

`PASSABLE` is now read only by that stale text (K8). Remove it together with F1.

**F6. AR invariants touched but not named in the commit (standing question 10).** The `architecture:` line names AR-24, 28, 13 and 14. It does not name:
- AR-18: the `run` result shape, and the `WORDS_REFUSED_AT_SOURCE … family` lines, which are now printed only for `open-oracle-asserted-*`;
- AR-22: `word_at`/`finding_id` have no reader until 30b (accepted by edge A3-E4; say so);
- AR-9: the door, see F1.

## Minor / queue

- **Q1 (K7).** The two detectors disagree for `unlinked-<instance>-<then>` and `ghost-<instance>`. A tag word passes the s5 finding, but `branch_accounting` still refuses "Then N is bound to no instance that covers it", because a Then with a row is never passed (`branch_accounting.py:1925`). The person is asked twice (FR-7). For `no-bindings`/`unbound-<n>` the detectors agree (traced). Queue a node: accept `unlinked-<inst>-<then>` when the row binds that instance; the Lead decides.
- **Q2 (K1, P31).** A second road remains inside S5. `branch_accounting` S5 records reach `exit_gate.judge_words` as `gate`/`named` (`exit_gate.py:1804`): `split_overridden` over the text, so a case-id word (`TC-1`) passes a "TC-1: … has no home" line. This is the t-108 class, traced, not run. Queue a node, axes 34/17.
- **Q3 (spec position defect, rule 11 (ii)).** Recording happens only inside `if d["stage"] == "S5" and p.get("stage_complete")` (`controller.py:5901-5909`), as the spec prescribes. An S5 window accepted with `stage_complete: false` (`open_windows`, `controller.py:5847-5851`) never records the passes of its own cases. The node's title says "every pass is recorded", so this is for the Lead to decide.
- **Q4 (K7, deviation 5).** Only `no-row-<iid>` lets `product:<iid>` go. That direction is right: an `unmatched` instance can carry a real red, and `product:` means only "outcome not passed" (`acceptance.py:1140`). The remaining cost: an `unmatched` instance with status `not_run` gets a second question at tier 4, and the `unresolved`+`reason` door remains. Queue.
- **Q5 (K5).** Adding `obligation-id` to the stage-wide stems passes only `obligation-id-<oid>` tags (no other tag starts with that prefix). It matches the writer: `manifest_put` already passes every `obligation-id:` refusal with that word. It is stage-wide with no time rule, so a word passes oids found later. The spec accepts that for findings with no `pair_at` (row "no `pair_at`: passes"). The fix is sound. Rename the constant: it is now "stage-wide stems", not "word-passable tags".
- **Q6 (K2, temporal).** A story already in flight that has text words recorded loses those passes: the person is asked again. The spec intends this. Add one changelog line: "a word recorded as a phrase of the line no longer passes; re-record it by the finding's tag".
- **Q7 (K4).** The other `then-remainder-*` tags (`shape`/`unknown`/`conflict`) wait for an author repair, not for something only a person can supply. Passing them is consistent with the owner's word. The fact stays downstream: `contract.then_remainder_rows` lists malformed rows "rather than dropped" (`contract.py:299-300`). `conflict` (proved AND left with the owner) needs the ledger/delivery reader checked. Add that to scout S-1's table. Not verified.
- **Q8 (process).** The builder ran two quarantined files (`test_row_fields`, `test_s5_precheck_plan`; TESTING.md: the builder neither runs nor edits a quarantined file).
- **Q9 (tests).** 426 test lines against about 250 product lines. The reason is the spec's input table. No new files, and the new functions are table-driven, so that part is fine. Killing power: see B1.

## K3 — the five red pins

| Pin | Layer | Origin | Owner decision behind it? | New expected value |
|---|---|---|---|---|
| test_row_fields K4 (h) | quarantine | 9ac00f0 (history cut at the import); pins "manifest outside PASSABLE" | none. The spec names it `known_red: FV1-30` (A3 row 1) and item 7 (`:391`) | `*` and `row-fields-missing` → 0 findings; `row-fields` and `manifest` → 1. Done by 30b item 7 or the quarantine rule, not 30a |
| test_s5_precheck_plan C12 | quarantine | 9ac00f0; SC1-14 B2 comment "family plan outside PASSABLE" | none; replaced by spec row 6, F-A3-2 (a) | `P._passable(f)` is True for every C12 finding. Same route as above |
| test_s5_precheck_sides S10 | keep | 5498318 (11.11); spec t-2181 `docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md:53,:140`: a design key, not an owner's word | none; replaced by the owner 13.11 + spec row 7 (Lead F-A3) | with `*` the kept `provisional-kind-*` list is `[]`; the tag word `provisional-kind-P-1` passes it; drop the `PASSABLE` constant check |
| test_then_remainder K3 | keep | 9ac00f0; spec t-052 key K3 (HF1-10/GW1-14) | the opposite: the GW1-14 finding (`plans/piles/gates-and-words/findings/20261022-odin-then-nelzya-otdat-cheloveku.md:28-29`) calls refusing the person's `partial-green` word a defect | with `partial-green` or `*`: `manifest:TC-700:partial-green` is passed and noted, no `family` line; with no word it stands and its fix still names `then handed:` |
| test_stand_gap_remedy `a_persons_word_passes_it` | keep | 9ac00f0; pins the text road (`remedy` = a phrase of the message) | none; replaced by spec items 2 and 3 | `match: "remedy-missing"` (the tag, `s5_precheck.py:3560`) → messages `""`, note kept; `remedy` → the finding stands |

None of the five needs a `NOT_PASSABLE_TAGS` entry. I found no carrier of an owner's word: DECISIONS.md and DECISIONS_ARCHIVE.md have 0 hits for `passable|partial-green|row-fields|provisional-kind|remedy-missing`. Positive controls: `waiver` gives 3 hits in the archive, `word|слово` gives 4 in DECISIONS.md.

## Standing questions

- **Fit (K1):** one selection rule ✓. The two waiting tags pass by nothing, `*` and whole id included ✓ (rows re-read). Selection is wrong in direction (B1). A second road remains in S5 through the gate records (Q2).
- **Builder decisions (K8):** `run(scope)` and `word_passes(dispatch_id)` are needed; with the controller's `d["scope"]` they give the cases of the same `dispatch_scope`. The three helpers are needed, but they duplicate id parsing (F3). `WORD_PASSABLE_TAGS` is live (`_names` stems). `PASSABLE` is dead in the logic (F5).
- **K6 recording:** one writer ✓. `word_at` ✓, `finding_id` whole on a cut ✓. Position after `_raise_all` ✓. A failure goes to stderr and the completion stays accepted ✓. F4 and Q3 remain.
- **K9:** AR-14 ✓, AR-24 ✓, AR-28 ✓ (readers that fail refuse), AR-29 ✓ (identity join, no reading of meaning), FR-12 ✓, FR-4 ✓. FR-45 fails under the judge (F2). AR-13 duplicated (F3).
- **JUDGMENT (Q11):** none moved into code. The diff adds no census row and no `blocks_override`.
- **DUPLICATION AND CONSISTENCY:** F3 (five id parsers, three of them new). Grepped `split(":", 2)` across `scripts/*.py`; positive control `_finding_tag` at `:4100` hit.
- **CODE QUALITY:** no new function is over 60 lines (`_judge_words` is about 45). Stale texts (F5). `_record_s5_word_passes` runs a full check even when there is no word (F2).
- **ONE ROAD (Q12):** none found in the diff by language, project or case (grepped the diff for language/runner names: none). The residual is Q2: a node with an owner, which the Lead opens.
- **Class completeness (K11, SIBLING_MAP axes 26/34/17):**
  - `exit_gate.judge_words` for `gate` records: same class. Queue (Q2).
  - `controller._passed_by_person`: same action, but over controller refusal lines that have no tag or id. The t-108 risk exists there too (a case id inside a line). Queue a node, axis 34.
  - `manifest_put._passed_by_word`: same class on the writer side; couples with K5. Queue together.
  - `window_record._unread_words`: per the builder it only prints and is no pass. I did not verify it. It is not in the class if that holds.

## Trail

- **Read:**
  - the spec §A3 (`:261-420`) and the builder report;
  - the full code diff (s5_precheck, controller, branch_accounting, changelog) and the test_s5_precheck and test_words_doors diffs;
  - `s5_precheck.py`: `:76-110`, `:440-499`, `:1240-1320`, `:1515-1625`, `:1715-1735`, `:1940-1975`, `:3890-3970`, `:4090-4101`, `:4174-4212`, `:4620-4665`, `:4678-4782`;
  - `contract.py`: `:134-160`, `:220`, `:293-315`, `:3924-3941`, `:4005-4086`;
  - `controller.py`: `:2389-2455`, `:5085-5100`, `:5140-5180`, `:5830-5931`, `:6498-6640`, `:6895-6914`;
  - `story_step.py:2250-2335`, `event_store.py` `_commit_locked`, `judge.py:357-394`, `exit_gate.py:1775-1815`, `acceptance.py:1115-1145`, `branch_accounting.py:1877-1970`;
  - the five red pins, test-layers.json, TESTING.md `:120-140`, critic-diff-brief.md, SIBLING_MAP axes 17/26/29/34;
  - plan carriers: GW1-14 finding, hotfix-12586 batches, t-2181 spec; DECISIONS greps.
- **P0:** `python -B …/fv130a/ai-packages/qa-factory/scripts/tests/test_s5_precheck.py` → `=== test_s5_precheck: 1057/1057 ok ===` (matches the witness).
- **P1:** `probe_names.py` (scratchpad) → e.g. `'run_mapping:TC_002:no-row-tests/api/test_books.py::test_create[neg]' word='neg' names=True`; `'bindings:TC_002:contradicted-literal-1-body.id' word='id' names=True`; `'oracle:TC_003:changed-after-red-a.py:12' word='12' names=True`; `'bindings:TC_003:no-bindings' word='bindings:TC_002:no-bindings' names=False`.
- **P2:** `probe_road.py` (scratchpad, `_judge_words` over a temp `pipeline.json`, word `missing-assistant`) → `passed: [run_mapping:TC-1:no-row-test_validate_per_partition[missing-assistant], manifest:TC-1:dup-…, bindings:TC-2:ghost-…]`, `standing: [bindings:TC-3:no-bindings]`.
- **P3:** `git log -S` on each pin line → 9ac00f0 (import) ×4, 5498318 (S10).
- **P4:** test-layers.json section per file → row_fields and s5_precheck_plan in `quarantine`; sides, then_remainder, stand_gap_remedy, s5_precheck, words_doors and branch_accounting in `keep`.

```json
{"verdict": "fit_with_fixes", "blockers": ["B1 s5_precheck.py:3950 _names calls names_whole(word, tag): a sub-identifier of a tag (partition label, parameter, line number, field leaf) passes findings the word never named (probe P2: 'missing-assistant' passed no-row/dup/ghost across two cases); fix: low == tag.lower() plus a test row", "B2 three keep-layer test files left red (test_s5_precheck_sides S10, test_then_remainder K3, test_stand_gap_remedy): batch canon red; widen owns and re-pin per the K3 table (TESTING.md: re-pin in the same node)"], "fixes": ["F1 s5_precheck.py:4727-4736 report tail: the door '<part of the line>' and 'no word passes any other finding' are false after 30a; print --block '<the finding's tag, or its whole id>' and the star clause with its two exceptions; blocks a separate merge to main", "F2 word_passes runs run() including passed_by_judge (judge LLM call and journal write under judge on/shadow) up to three times per completion; take the passes before the judges and return [] early when no live S5 word", "F3 finding_id parsed with split(':', 2) at controller.py:7365, branch_accounting.py:1929, s5_precheck.py:4045; pass rows carry check/case/tag fields", "F4 controller.py:6505 _plan_refusal records inside validate (story_step probe at story_step.py:2329, refused requests, repeats); drop and queue, or record after commit", "F5 stale docstrings and comments claiming families are not passable (s5_precheck.py:80-88, 95-98, 1520, 2372, 3812, 3961-3963, 4556, 4616, 4633, 4725); PASSABLE is now dead in the logic", "F6 the commit architecture line misses AR-18, AR-22 and AR-9"], "class_completeness": "Same class, queued as nodes for the Lead: exit_gate.judge_words gate records of branch_accounting S5 (text road, t-108 class; axes 34/17), controller._passed_by_person (axis 34), manifest_put._passed_by_word (couples with K5); window_record._unread_words prints only (builder claim, not verified, not in the class if so). Detector disagreement for unlinked/ghost (Q1) and recording only on stage_complete S5 acceptances (Q3, spec position) are queued for the Lead.", "trail": {"read": ["docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:261-420", ".claude/worktrees/fv130a/docs/tasks/specs/reports/20261113-fv130a-report.md", "git diff 5c16666 a4fc87b -- ai-packages/qa-factory", "scripts/s5_precheck.py (ranges in Trail)", "scripts/contract.py:134-160,293-315,3924-3941,4005-4086", "scripts/controller.py:2389-2455,5085-5100,5140-5180,5830-5931,6498-6640,6895-6914", "scripts/story_step.py:2250-2335", "scripts/judge.py:357-394", "scripts/exit_gate.py:1775-1815", "scripts/acceptance.py:1115-1145", "scripts/branch_accounting.py:1877-1970", "scripts/tests/test-layers.json", "docs/TESTING.md:120-140", "docs/tasks/critic-diff-brief.md", "docs/SIBLING_MAP.md axes 17,26,29,34", "plans/piles/gates-and-words/findings/20261022-odin-then-nelzya-otdat-cheloveku.md", "docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md:53,140"], "reruns": [{"command": "python -B .claude/worktrees/fv130a/ai-packages/qa-factory/scripts/tests/test_s5_precheck.py", "result": "=== test_s5_precheck: 1057/1057 ok ==="}, {"command": "python -B scratchpad/probe_names.py", "result": "word 'neg' names no-row-...[neg]; 'id' names contradicted-literal-1-body.id; '12' names changed-after-red-a.py:12; sibling whole id does not name no-bindings"}, {"command": "python -B scratchpad/probe_road.py <tmp story>", "result": "word 'missing-assistant' passed run_mapping no-row, manifest dup, bindings ghost (two cases); no-bindings stood"}]}}
```
