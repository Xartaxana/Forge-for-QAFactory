# Rules-debt phase 2 — builder cards S9, FL2, FL4 (t-995, F19)

Designer draft for the Lead. It answers plan critic t-989 (`docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md`,
sections S9, FL2, FL4, K6, K8). The cards spec `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` was read, not
written. Parent spec: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (S9 :379-394, F-L2/F-L4 :538-544).

**Where the code was read.** The root checkout, branch `main`, head `a6df7fd1` (git status at session start). The critic
read `origin/main` = `a372b01a`. The lines the critic gives match this tree: `controller.py:7421 _s5_word_index`, `:7440
_s5_gap_problems`, `:9387 ANSWER_REWORK_OWNERS`, `:9904 --cases`, `window_record.py:1741 WORD_READ_KINDS`, `:1745
_unread_words`, `:1766`, `:1891` (Grep, this session). So the line numbers below hold for both trees. No Bash was
available to this designer, so **no command was run**. Every measurement below is a reading with file:line. Where a run is
owed, the card names it as the builder's step 0.

**Budget.** The AGENT BUDGET WARN fired at 255K tokens, while the S9 research was finished. S9 is drafted to builder
level. FL2 is drafted with its direction and one open fork. FL4 is **not drafted**: its research (the S7 rework route
code, `no_move.check_args`, `answer_pairs_owed`, `check_delivery` bug_candidate readers) was not done. The handover list is
in §5.

---

## §1. Architecture, rules, owners (designer rule 1)

FR sections: S9 A (FR-4, FR-57), B (FR-7, FR-8), D (FR-59), E (FR-35). FL2 E (FR-21, FR-35), C (FR-12, FR-13).

| card | AR-n touched | how kept (the change check written into the DoD) |
|---|---|---|
| S9 | AR-13 | the person's word on a `review` gap has ONE reader, `window_record.review_gap_words`, and every judge reads it through `word_let_go`; no judge reads `stage_overrides[]` for it by itself |
| S9 | AR-15 | the one predicate `window_record.word_let_go` gains the rule, so all five judge sites (controller ×1 for gaps, `word_kept` → `window_record.run`, `story_step finish`, `driver_dispatch`) agree with no wiring of their own |
| S9 | AR-24 | the person's words reach the pass record whole (`_record_person_pass` keeps `word_at`; the report reads the word by `at`) |
| S9 | AR-25 | the new recorded state "review gap passed by a person's word" has its way out: the next window build (a critic verdict written) removes the gap, and the pass line in the report goes too (`_word_bare_lines` reads facts) — row in `design/state-exits.md` |
| S9 | AR-27 | the delivery reason keeps its owner `review` (verdict `no`); the pass shows as its own line in "passes recorded by your word" |
| S9 | AR-28 | `review_gap_words` errs toward NO entry: an unreadable pipeline, `*`, a revoked word, another stage, a placeholder word → nothing is let go |
| S9 | AR-9 | the door text of the `review` gap (`GAP_ORIGIN["review"]`, `window_record.py:318-320`) names the person's road |
| FL2 | AR-13, AR-22, AR-26 | see the FL2 card (fork F-L2-A decides which applies) |

Checks added or altered (AR-29, census classes of `scripts/tests/fixtures/judgment-census.json`):

| check | card | owner it serves | census class | blocking |
|---|---|---|---|---|
| `window_record.review_gap_words` + the `review` rule of `word_let_go` (a person's word lifts a window gap) | S9 | intent (the person's word, P13) | xref (a join of the word to the gap by an identifier; the class `contract.probe_gap_words` / `word_let_go` already carry — the builder copies the class of the `word_let_go` row of the census; when the census has no such row, the builder returns a question naming the missing row) | lifts a block, never adds one |
| FL2's skip class | FL2 | judgment (the S3 strategist picks the class; a tier above accepts it at the S3 window) for the word; data for the mapping | shape (the kinds-file lookup), if F-L2-A (b) | blocks delivery (`no`) |

Commit lines: the form is `tools/architecture_gate.py`'s (not copied here). Content for S9:
`architecture: AR-13, AR-15, AR-24, AR-25, AR-27, AR-28 -- <how kept, from the table>`; `judgment: adds data check
review_gap_words` (the gate's own vocabulary decides the exact form; `judgment: none` is not legal here because a check
is added).

---

## §2. S9 — X10: a person's word on a `review` gap (FR-57)

### 2.1 Measured premises (PROJECT.md «Как принимается изменение пакета» п. 6 (а))

| # | premise | carrier | result |
|---|---|---|---|
| P-a | a person's word on a `review` gap happens on real runs | `scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json:615-635` | **yes**: three live S5 records, `match` = the whole window line `review:@regression LOCAL-1_TC_001 in-stock add shows success toast, badge 1 and one cart line — the manifest row carries no \`critic_verdict\`` (and two more for TC_002), `by: human`, words "go on … They stay unverified in the report." |
| P-b | the person also typed `*` on the same window | same file `:678-684` | **yes**: `match: "*"` at 15:53:20, after the three review words (15:49) — the hostile input of F-9-4 occurs in real data |
| P-c | instance ids carry spaces | same file `:617-631` | **yes** (Playwright titles). So the one-token prefix road (`contract.prefix_value`, `contract.py:121-132`: "must be a single token") **cannot** name these instances; `probe gap:` words on the same run named CASE keys (`:687`, `:695`) |
| P-d | today nothing reads such a word | `window_record.py:1741` (`WORD_READ_KINDS = ("quality", PROBE_GAP_KIND)`), `:1891-1892` (only those kinds join `read`), `:1912` (`_unread_words` over every line not in `read`), `GAP_ORIGIN["review"]` comment `:314-317` ("NO recorded word of a person passes this gap"); `word_let_go` keeps `review:` lines, pinned `test_window_record.py:1847-1850` | **yes, by reading**. Not run: no single recorded fixture has both a window and a review word (`local-1-arm-b` has no `work/automation-manifest.json` and no `work/windows/` — Glob over `local-1-arm-b/**/*.json`, 34 files, none; `cart-1/work/windows/` has six windows and no `review:` word in `cart-1/pipeline.json` — Grep `"match":` lists all 15 cart-1 matches, none `review:`). Step 0 of the card makes the run |
| P-e | the existing "a word passes a window line" road | `window_record.py:1242-1289 word_let_go` ("THE one predicate", AR-13, AR-15); callers `controller.py:7122`, `:7522`; `window_record.word_kept` `:1292-1310` → `window_record.py:2185`, `story_step.py:2563`, `driver_dispatch.py:1018` (Grep `word_let_go\(|word_kept\(` over scripts) | five judges, one predicate |
| P-f | delivery today for a test with no critic verdict | `ledger.py:1183-1185` → `review_skipped`; `ledger.py:1630`, `check_delivery.py:1676-1679` → kind `review_gap`; `delivery-verdict-kinds.json:35` `review_gap: no, owner review`, `:100-102` | `no`, owner `review` |
| P-g | the precedent "the word passes the STEP, never the FACT" | `delivery-verdict-kinds.json:3` note (`word_passed:then_unbound` keeps `chain_broken`, `no`); `check_delivery.py:1640-1658 _no_run_word_suffix` (a `not_run` pass keeps its `no` row, adds "passed by the person's word at S5"); `report_facts.py:3291-3363` (every recorded pass gets a line; fact `other` via `_word_bare_lines`, `:3360`) | the precedent exists twice |
| P-h | the precedent for "the person's word moves the test into their debt" | `window_record.py:344-351` (`probe_gap`: "S8 reads it as the critic's `unverified` ('Left with you')"); `ledger.py:1213-1217` `review_unverified` → `after_checks` (`delivery-verdict-kinds.json:58`) | exists for probe gaps, not for reviews |

### 2.2 Direction (chosen; forks F9-1 and F9-2 in §4)

1. **Which road.** The review rule joins **`word_let_go`** (P-e): one predicate, all judges. It is not a third road
   beside `WORD_READ_KINDS`/`probe_gap_named` (critic F-9-6, P31).
2. **Which matcher** (critic F-9-4). A NEW reader `window_record.review_gap_words(window, task_root) -> dict`
   `{instance id: {"words", "at"}}`, built on the two primitives every word reader already uses: the filter
   `contract.live_stage_overrides(pipeline, ("S5",))` (`contract.py:158-174`: revoked and empty words out) and the
   predicate `contract.names_whole` (`contract.py:135-155`). Rule: an instance `iid` of `window["instances"]` is
   named when a live S5 record's `match`, stripped, is NOT `*`, does NOT hold a `<placeholder>`
   (`waiver.PLACEHOLDER_RE`, the rule `split_overridden` applies, `waiver.py:210-211`), and
   `contract.names_whole("review:" + iid, match)` is True. The latest record by file order wins (`words` = its
   `decision` whitespace-folded, `at` = its `at`). The pipeline is read from `task_root / "pipeline.json"`, never from the
   window (a role writes the window). Why not `waiver.split_overridden` itself: it reads `*` as everything
   (`waiver.py:205`, `:217`), and it asks "is the WORD whole inside the LINE". The controller's lines are bare
   (`review:<iid>`, `acceptance.py:1157-1172`), so a word that is the whole printed line (P-a, the real data) is never
   inside the bare line, while `window_record.run`'s lines carry the explanation. Asking "does the word name the gap
   head `review:<iid>`" gives the same answer at every judge, whatever the line form. This is the same direction as
   `contract.probe_gap_words` (word → identifier, `contract.py:5648-5659`).
3. **What the pass does to delivery** (critic F-9-3): **reading (i)**. The word passes the S5 STEP. The ledger is
   untouched, so the test still reads `review_skipped` / `review_rejected` → `review_gap` → `no`, owner `review` (P-f).
   The pass is recorded and the report shows it in "passes recorded by your word" (P-g). FR-35 holds, because the
   critic's verdict, or its absence, is never rewritten. This is fork F9-1, recommended (i). The card is executable on
   (i). (ii) would add a ledger state and a kinds row later. The ledger is not in S9's owns.
4. **Recording**: `controller._s5_gap_problems` writes one `_record_person_pass` line per let-go review gap, ONLY when
   the completion is otherwise accepted (`not problems`), the precedent `controller.py:7527-7534`.

### 2.3 Card S9 (header-ready)

```
given: this file §2; docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md (S9 section);
  ai-packages/qa-factory/design/factory-rules.md (whole); plans/builder-rules.md; ai-packages/qa-factory/design/architecture.md
  (AR-13, AR-15, AR-24, AR-25, AR-27, AR-28); scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json:615-700 (the world)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py (review_gap_words [new], word_let_go, word_kept, verdict, GAP_ORIGIN["review"] text and its comment :314-320, the WORD_READ_KINDS comment :1732-1740)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (_s5_gap_problems only) — HOT
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py (rows in fv1_30b_word_let_go_is_the_one_predicate and one new row function beside it)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_gap_word.py (one row: the controller end to end)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (the row of review_gap_words only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md (one row)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (regenerated by tools/controller-blocks-gen.py only if a block text of _s5_gap_problems changes)
non-goals: ledger.py, check_delivery.py, delivery-verdict-kinds.json, waiver.py, contract.py, acceptance.py (no change: reading (i));
  the `*` meaning anywhere else; the not_run / row_fields rules of word_let_go; the run() line-form observation O-1 (§5)
handoff: the builder report (builder.md rule 7) with the witness, the FR walk (A, B, D, E), the census row, and step 0's output
edges: E1-E12 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` — the slow files it names
  (test_window_record.py, test_probe_gap_word.py, test_controller_*) are named "judged by the batch canon"; plus
  `python -B tools/architecture_index.py --check`
siblings: axis 26 (n/a by design: the word is not split_overridden's — reason in §2.2 item 2, stated in the
  review_gap_words docstring); axis 32 (census row, owned); axis 34 (the word_let_go road, no third road); axis 5 (S5
  windows <-> S6 walker lanes: no S6 twin reads a review word — the builder confirms with one Grep for
  `word_let_go` over driver_stage_s6.py, positive control: the same Grep finds it in driver_dispatch.py)
designer: <this file, once accepted>
```

**Step 0 (premise run, before any edit; output goes into the report).** In the scratchpad copy `cart-1` whole. In the
copy's `pipeline.json`, add one S5 record whose `match` is `review:<iid>`, with `<iid>` = an instance of
`work/windows/S5-qa-code-critic-2.json` whose `review.verdict` is not `approved`. If none is non-approved, delete that
instance's `critic_verdict` in the copy's manifest. Then run `python -B <pkg>/scripts/window_record.py --task <copy> --dispatch S5-qa-code-critic-2 --out <scratch>/w.json`.
Expected on today's code: the gap line `review:<iid> — …` is listed, and a `note: recorded, not read by this window: …`
line names the word. If the line does not appear, the builder stops and returns the output (the premise is false, and
the Lead re-plans).

**Items** (each with its test row and the source of the expected value):

1. `review_gap_words(window, task_root)`, per §2.2 item 2. It never raises: anything that is not a dict, an unreadable
   or absent `pipeline.json`, or any exception → `{}`. Test: a table row in a new function
   `s9_review_gap_words` in `test_window_record.py`, one row per input of E1-E6. Expected from the debt row FR-57
   (`factory-rules-debt.md:85`), the parent spec S9 (в) (`20261117-rules-debt-fix-spec.md:384-387`), and critic F-9-4.
2. `word_let_go(lines, window, index, lets_go=None, review_words=None)`: a third rule. For each instance `iid` of the
   window that is in `review_words`, the line `review:<iid>` is let go, and so is any line that starts with
   `review:<iid> — ` (the `verdict` form, `window_record.py:1868`). `review_words=None` lets no review line go (the
   refusing default; every existing caller is unchanged until it passes the argument). The `index is None` early return
   (`:1260-1261`) must NOT skip the review rule. The invariant is that a broken precheck index does not hide a person's
   word, and that a broken word read does not let anything go. So: if `index` is None, the not_run and row_fields rules
   let nothing go, and the review rule still runs. The docstring names the third rule. Test: rows in
   `fv1_30b_word_let_go_is_the_one_predicate`. The existing pin `"review:i" in kept` (`test_window_record.py:1847-1850`)
   stays true with `review_words` absent. New rows: a word naming `i` lets `review:i` go; `stale_review:i` is kept
   (another kind); `review:i[neg]` is kept (a parameter sibling); `review_words` given + `index=None` lets `review:i`
   go and nothing else. Expected: the same sources plus `word_let_go`'s own docstring invariant ("Every other line is
   kept").
3. `word_kept(...)` passes `review_words=review_gap_words(window, task_root)`. This wires `window_record.run`,
   `story_step finish` and `driver_dispatch` with no edit of theirs. Test: one row beside `test_window_record.py:2522`
   (`word_kept` over `["review:A"]` with a pipeline holding `review:A`) → `([], ["review:A"])`.
4. `verdict(...)`: a `review` line whose instance `review_gap_words` names joins `read` (`:1891-1892`), so
   `_unread_words` no longer prints "recorded, not read" for a word that IS read. A `*` word, or a word naming the reason
   only, is still printed as unread. Test row: `info` holds no "recorded, not read" line for the naming word, and still
   holds one for `*`. Expected: the `_unread_words` docstring (`:1750-1751`: "never passes a gap nobody reads it for").
5. `GAP_ORIGIN["review"]` door text (`:318-320`) adds the person's road: `… or, when the person accepts the test without
   the critic's verdict, the orchestrator records their words with \`waiver.py --task <T> --stage S5 --block
   "review:<instance id>"\` (the S5 step passes; delivery still reads no critic verdict)`. The comment `:314-317` and the
   `WORD_READ_KINDS` comment `:1732-1740` are rewritten to say the review word is read through `word_let_go`. Test: one
   `check_in` row on `WR._explain("review:x", [])` for `--block "review:`. Expected: FR-2 and AR-9 (a door the receiver
   can use).
6. `controller._s5_gap_problems` (`controller.py:7520-7535`): the call `word_let_go(other_gaps, window,
   self._s5_word_index(d))` gains `review_words=window_record.review_gap_words(window, self.store.root)`. After the
   refusals, when `not problems`, every let-go line that starts with `review:` gets one `_record_person_pass("S5",
   d.get("id"), [...])` item: `{"error": "review:<iid>", "decision": words, "at": at, "by": "human", "check": "review",
   "case": "", "tag": <iid>, "subjects": [{"instance_id": <iid>}]}`. Test: one row in `test_probe_gap_word.py` (it already
   drives `_s5_gap_problems` end to end with `PASSED_BY_PERSON`, `:51`, `:145`): a window whose only gap is `review:IID`,
   plus the word → accepted, and ONE line in `passed-by-person.jsonl` with `block` `review:IID` and the words whole;
   the same window with `*` instead → refused "unresolved window: review:IID". Expected: FR-4 ("a check stops a silent
   pass, never an informed one"), P13, and the precedent `:7527-7534`.
7. `design/state-exits.md`: one row: state "S5 review gap passed by the person's word"; exit = a critic verdict
   recorded later removes the gap (the next window has none) / the word revoked (`waiver.py --revoke`) → the gap
   refuses again. Doc only; the witness is the DoD key run (CLAUDE.md rule 11 DOC-DISPATCH WITNESS) or the walker
   row if `scenario_walk.py --witness-for` names one.
8. Census: one row for `window_record.review_gap_words`, class per §1. `word_let_go`'s existing row (if any) changes its
   note only.

**Edges (rule 11), each with the invariant it protects:**

- E1 `*` (P-b, real). → not read. INVARIANT: a stage-wide word never lifts a review gap. (Critic F-9-4.)
- E2 a revoked record (`revoked_at`) naming the gap → not read (`live_stage_overrides`). INVARIANT: a word taken back acts
  nowhere (FR-40).
- E3 a word of another stage (S6) naming `review:<iid>` → not read. INVARIANT: an S5 gap is passed only by an S5 word.
- E4 a word naming another instance: `review:A` vs instance `A[neg]`, and vs `B`; a word naming `sensitivity:<iid>`; a
  word naming only the reason tail ("the manifest row carries no `critic_verdict`"); a bare `<iid>` or a case key → not
  read. INVARIANT: only a word that names THIS gap head lifts it (`names_whole` right edge, `contract.py:141-145`).
  (Fork F9-2 asks whether a case key should also count. The recommendation is no.)
- E5 empty input: a window with no `instances`, an empty `stage_overrides`, a pipeline that is not an object, an absent
  `pipeline.json`, unreadable bytes → `{}`, nothing let go. INVARIANT: an unknown is never a pass (AR-28, FR-59).
- E6 a `match` holding a `<placeholder>` (an unfilled door) → not read (the `split_overridden` rule, `waiver.py:211`).
- E7 limit / truncation: `_record_person_pass` cuts `block` at 400 and `decision` at 1000 (`controller.py:2425-2426`) and
  keeps `word_at` and `finding_id` for the whole (`:2432-2435`). An instance id over 400 chars → `finding_id` carries the
  whole block. INVARIANT: the cut loses nothing the report needs (AR-24). No new limit.
- E8 CONFLICT with the critic's own verdict: the gap stands for `rejected` too (`acceptance.py:1171-1172`). A word naming a
  rejected instance lets the S5 step go (P13: through any gate). The ledger still reads `review_rejected` → `no`
  (`ledger.py:1189-1190`). INVARIANT: FR-35, the report never changes the critic's verdict. In `window_record.run`, the
  let-go happens before `_sent_back_lines` (`:2235`), so a word-passed rejected instance is not sent back. That is
  the person's decision, recorded.
- E9 POSITIONAL (`word_let_go`): the review rule runs even when `index is None`. INVARIANT: the not_run and row_fields
  rules still let nothing go on a None index (pinned `:1832`), and the review rule depends only on `review_words`.
- E10 POSITIONAL (`_s5_gap_problems`): the record is written only after every refusal of the method ran and none fired,
  and is never written for a refused completion. INVARIANT: no pass line for a window that did not close (the probe_gap
  precedent). `passed_green` keeps reading the whole `gaps` (`:7525`). INVARIANT: a word-passed review never makes a
  `passed_green` completion legal.
- E11 TEMPORAL: windows and pipelines written before S9 have no new field and need none. The reader reads existing
  `stage_overrides[]` records, so the three words of a story in flight (P-a shape) start to act on the next judge after
  the upgrade. That is intended: they were recorded as words and promised to pass (debt row cost line). An OLD
  `passed-by-person.jsonl` with no `review:` line reads as before. Nothing is rewritten (builder-rules 9).
- E12 outside input: the `match` text is the person's (through `waiver.py`). Battery rows in item 1's table: magnitude
  (a 10 000-char match), nesting (n/a, a string), encoding (a non-ASCII instance id, a match with `\u2014`, which is the
  verdict separator), empty / blank / non-string `match` → not read, never raises. The 400 cut is E7.

**Reused function in a more responsible role.** `contract.names_whole` moves from advice (`_unread_words`, reporting) to a
gate input. The error it may make is toward False (it then asks the person again). Adversarial inputs that must stay
False: E4's list, plus `review:A` inside `review:AB`, `review:A.1`, `review:A::x`, `review:A[`, and `review:A@x`
(`contract.py:141-145`). `contract.live_stage_overrides` keeps its role (a filter).

**FR walk the builder writes** (PROJECT.md p. 1): A FR-4 (informed pass recorded), FR-57 (the ban now has a door), FR-2
(the door is usable: the conductor records it); B FR-7 (the same boundary is not re-asked: the word is read), FR-8
(words carried whole); D FR-59 (unknown → no pass); E FR-35 (critic verdict unchanged); C, F, G one line each.

**Live proof (FR-33):** a `live-runs` row "a person's `review:<iid>` word at S5 lets the window close; the report shows
the pass and delivery `no` owner review". Reading the `waiver.py` CLI's acceptance of the block text is part of it. NOT
ESTABLISHED by reading: whether `waiver.py`'s recheck holds `review:<iid>` against the standing refusal (`waiver.py:225-252`).
The tests write the record with `waiver.apply_stage_override` the way `test_controller_release.py:516` does.

### 2.4 Readers of every touched file (rule 7)

The S9 readers of rule 7 were not grepped this session (no Bash; the budget ran out first). The command for the Lead
or the builder: Grep over `tools/`, `.githooks/`, `.claude/` for
`window_record|controller\.py|state-exits|controller-blocks|judgment-census|test_window_record|test_probe_gap_word`.
Positive control in the same shape: `architecture_gate` in `.githooks/commit-msg`. The known readers from the cards
spec §8 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:773`): `tools/controller-blocks-gen.py` reads
`controller.py`. It changes in S9 only if a block text of `_s5_gap_problems` changes, and item 6 changes none. Package
readers of `word_let_go`/`word_kept` (P-e): `story_step.py:2563`, `driver_dispatch.py:1018` are unchanged (the new
argument is passed inside `word_kept`); `controller.py:7122` (shape call) is unchanged (`review_words` stays None, and
review is not a shape line).

### 2.5 Collisions

- `controller.py` HOT: S9 owns `_s5_gap_problems` only. FL4 (not drafted) owns the rework route (around `:3779-3789`,
  `:9387`, `:9904`). These are function-disjoint, so they can run in parallel by D-0048 if FL4's owns list names no S9
  function. Otherwise the queue is `S9 → FL4`.
- `window_record.py`: C3-d (after S9, critic F-d1) touches `verdict`. Queue `S9 → C3-d`.
- `judgment-census.json`: `wave-a/integrate` (unmerged) edits it (critic F-S4). S9 starts after that merge (S-e).
- `test_window_record.py`, `test_probe_gap_word.py`: slow (cards spec §0.3). Rows only, with no new test file, so
  `test-layers.json` is untouched. `pile/live-run-fvf/batch-3` (dry_*, fixtures, slow_tests.json): no overlap, because S9
  only reads `local-1-arm-b` and copies `cart-1` into the scratchpad.
- Taken batches (cards spec §4): onboarding-forge/2 names `window_record` and `controller` rows. Lead decision 17.11:
  dev1's batches do not hold each other.

---

## §3. FL2 — R3: "skipped because the product has no such surface" (FR-21)

### 3.1 Facts

- The writer is the S3 PLAN row: `disposition: skip` with a free `reason` → `ledger.py:763-773` returns
  `skipped:<reason>`. The kinds lookup reads the prefix `skipped` → `planned_skip` (`delivery-verdict-kinds.json:95`,
  `:21` `none`). The run-row form `skipped:marked skipped in the run` (`:94`) is `decided_elsewhere` (critic F-L2-1,
  re-read today).
- The existing road for "the product does not carry this yet": manifest `unresolved: [{case, reason:
  "pending_implementation"}]` → `ledger.py:731-732` → state `pending_implementation` → kind `no`, owner product
  (`delivery-verdict-kinds.json:44`, `:97`). It is read per CASE (`_cases_for_row`, `ledger.py:707`). A plan row with
  no case is never reached by it: the loop `for case in cases` (`:716`) is empty for a row that S4 never cased, and a
  `skip` row gets no case.
- Premise (critic F-L2-2): 3 skip rows over the recorded plans, 1 of class R3 (`local-1-0108/work/test-plan.json`, "the
  owner's answer leaves no implemented quick-view add path …"). The critic counted by a script, and it was **not re-run
  here** (no Bash). Re-run command for the builder's step 0: a short Python run over
  `scripts/tests/fixtures/stories/*/work/test-plan.json` counting `disposition` and printing the `reason` of each
  `skip`. Expected `96 automate, 58 gap, 3 skip, 5 unverifiable`.

### 3.2 Why the existing road cannot carry it as is (critic F-L2-3, P31)

The `pending_implementation` road is written at S5 (the automator's manifest) or by grounding, and it keys on a case. A
row the strategist skips at S3 never reaches S4/S5, so no case and no manifest row exist for it. **One road is still
possible**: the S3 strategist writes the existing word `pending_implementation` as the plan row's closed class (not a
new word), and the ledger's skip branch reads it into the existing state `pending_implementation`. The kind, the owner
and every reader downstream stay the existing ones. No new kind, and no new kinds-file word.

### 3.3 Direction and fork

- **Fork F-L2-A** (§4): (a) a closed field `skip_class` on the plan row with the ONE value `pending_implementation`
  (the existing state word). `ledger.py:771-772` returns `("pending_implementation", "")` for a `skip` row carrying it,
  before the free-reason branch. The kinds file is unchanged; the producer is the strategist charter plus the plan
  contract (`planning_contract`). (b) the critic's shape: a new word `skipped:<word>` → `pending_implementation` in the
  kinds file. That opens a second spelling of one fact (P31). **Rec (a).** Cost of (a): a plan contract field. That
  contract is the `planning_contract` file, which `wave-a/integrate` edits (brief), so FL2 queues after that merge, as
  well as after C3-e/C3-R.
- The card is **not executable until the owner's word**, because it changes the meaning of a delivery word (PROJECT.md
  п. 6 (б): plan critic on this text). Also, the producer files (strategist charter, `planning_contract.py`) were not
  read this session.

### 3.4 Card FL2 (partial: header lines the Lead can fill after F-L2-A)

```
owns (on F-L2-A (a); function names to confirm by reading — NOT read this session):
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (the skip branch of the plan-row state, :763-773)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/planning_contract.py (the plan row field check) — after wave-a/integrate
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-test-strategist.md (one line: when to set skip_class)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py (one L-row: a skip row with skip_class -> pending_implementation -> no)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (own row)
edges: E1 skip_class absent (every old plan, TEMPORAL) -> today's `skipped:<reason>` -> planned_skip; INVARIANT: no old
  plan changes its verdict. E2 skip_class with a value outside the closed set -> refused by the plan contract with the
  allowed value named (FR-1); INVARIANT: an unknown class is never read as planned_skip. E3 skip_class on a non-skip row
  -> refused (the class belongs to a skip). E4 POSITIONAL: the check sits after `_placeholder_reading` (:766-769), so an
  open placeholder still wins (the J-C7 invariant), and before the free-reason return. E5 the reason text is never parsed
  (FR-12).
DoD: scenario_walk.py --witness-for <owns>; the slow test_third_verdict.py is judged by the batch canon
siblings: axis 34 (one road: the existing state word); axis on the delivery verdict (SIBLING_MAP:144 readers unchanged)
```

Readers of the touched files (rule 7): not grepped (budget). The command is the S9 one with `ledger|planning_contract|qa-test-strategist`.

---

## §4. Forks returned (t-995)

| id | question | options | recommendation | card executable on the rec until the owner's word? |
|---|---|---|---|---|
| F9-1 | what the person's word on a review gap does to delivery (critic F-9-3; P13 vs P21 vs FR-35) | (i) passes the S5 step only; delivery `no`, owner review, with the pass line shown (precedents P-g); (ii) a new ledger state / kind: `after_checks` (the person's debt, like `probe_gap` → `review_unverified`, P-h) for a MISSING verdict, `rejected` stays `no` | **(i)**: no ledger or kinds change, FR-35 intact, two precedents. (ii) is one later node (a ledger branch + one kinds row) if the owner wants a word-passed review to stop holding delivery | **yes** (the owner's word decides (ii) later; (i) is a subset of (ii)'s code) |
| F9-2 | does a case-key word (`LOCAL-1_TC_002`) also pass the review gaps of its instances? | (a) no: only a word naming `review:<iid>`; (b) yes: also a case key that `scope_instances` lists for the instance (the `probe_gap_named` join, `acceptance.py:1019`) | **(a)**: the door prints the exact head to copy, and the real record (P-a) used that form 3 of 3. (b) widens one word to several tests | yes |
| F-L2-A | how a skip "because the product lacks it" is typed | (a) closed `skip_class: pending_implementation` read into the existing state; (b) a new kinds word `skipped:<word>` | **(a)** (P31: no second spelling) | **no**: a delivery meaning change (plan critic on this text first), and the producer files were not read |
| F-L4-? | FL4 forks | not drafted | — | no |

Closed by me (no design weight): the pass record uses fact `other` (no new `word-passed-facts.json` row), because the
report already lists `other` passes (`report_facts.py:3360`). The new reader lives in `window_record.py`, next to its one
consumer, and not in `contract.py`. The test rows go into the existing functions of slow keep files, with no new file.

---

## §5. Not done — handover (budget stop at about 255K)

1. **FL4 — not drafted.** Left: read `controller.py:3760-3800` (the refusal and its comment), `no_move.check_args`,
   `answer_pairs_owed`, `check_delivery.py:2363-2367` (`bug_candidate_record`, `"case": ""`), `grounding_records`, the S8
   reporter's triage reader, `controller-blocks.md` rows for the rework route, and `ANSWER_REWORK_OWNERS`
   (`controller.py:9387`: today `strategist → --rows`, `designer → --cases`; no analyst entry, read today). Then draft the
   route `--operation rework --candidate <K-n>` (S7 only), its refusal invariant ("an empty S4+ case list without a
   candidate is still refused"), the triage row key for a case-less candidate, both TEMPORAL worlds (triage rows and
   candidate records without the key), and the owns as functions disjoint from S9's `_s5_gap_problems`. Critic F-L4-1
   lines re-verified today: `:9387`, `:9904`.
2. **S9 rule 7 grep and FL2 rule 7 grep**: the commands are given (§2.4, §3.4). They were not run.
3. **FL2 producers**: read `planning_contract.py` (after the wave-a merge), `agents/qa-test-strategist.md`, and the
   `test_s1_s2_contract.py` G1-10 reader (quarantined, read only).
4. **Observation O-1 (an analog noticed, not widened)**: `window_record.run` calls `word_kept(problems, …)` on lines
   that carry ` — <explain>` (`verdict` `:1868`), while `word_let_go` matches the exact `<kind>:<iid>` (`:1277-1285`).
   The not_run and row_fields rules may therefore let nothing go in `run()`, while they work in the controller and in
   finish (bare lines). This was found by reading and not run. S9's own rule matches both forms (item 2). The sibling is
   a finding for the Lead (needs one run).
5. The critic's census class for `word_let_go` was not read in `judgment-census.json`. Item 8 tells the builder to copy
   it or return a question.

## §6. Critic finding → where answered

| finding | answered |
|---|---|
| F-9-1 no plan | §2.2, §2.3 items 1-8 |
| F-9-2 premise unmeasured | §2.1 P-a..P-h (by reading, with carriers); the run is step 0 (no Bash here) |
| F-9-3 delivery effect | §2.2 item 3; fork F9-1 |
| F-9-4 `*` vs split_overridden | §2.2 item 2; E1, E4; reused-function paragraph |
| F-9-5 lines drifted | header: 7421/7440 confirmed |
| F-9-6 axes 26/32/34 | card `siblings:`; §1 census row |
| K6 (S9) | §2.5 |
| F-L2-1 writer | §3.1 |
| F-L2-2 premise | §3.1 (the critic's count; re-run command given, not run) |
| F-L2-3 second road | §3.2, F-L2-A |
| F-L4-1, F-L4-2 | **not answered** (§5.1) |
| K8 axis 5 (FL4) | not answered |

**Order**: S9 first (after the `wave-a/integrate` merge, for the census). C3-d and FL4 come after S9; FL4 can run in
parallel with S9 if its owns are function-disjoint. FL2 runs after C3-R (C3-e) and after the wave-a merge
(`planning_contract`), and only on the owner's word for F-L2-A. In parallel now: S9 alongside C3-R; FL4's design draft
alongside both.

## §7. Reading trail

Read: the critic review t-989 (whole); cards spec `:1-76`, `:520-609`, `:640-852`; parent spec `:370-399`, `:525-662`;
`factory-rules-debt.md:15-89`; `window_record.py:140-169`, `:300-380`, `:1170-1315`, `:1725-1925`, `:2170-2280`;
`controller.py:2400-2489`, `:6990-7120`, `:7380-7567`, `:7680-7756` (+ Grep 3994, 7421, 7440, 9387, 9904); `acceptance.py:999-1039`,
`:1130-1179`; `contract.py:115-204`, `:5630-5690`; `waiver.py:202-252`, `:740-1050`; `s5_precheck.py:4060-4130`; `ledger.py:700-779`,
`:1150-1229`, `:1610-1674`; `check_delivery.py:1615-1694`; `report_facts.py:3285-3375`; `delivery-verdict-kinds.json` (whole);
`word-passed-facts.json` (whole); `block-names.json` (whole); `SIBLING_MAP.md:115-144`, `:448-457`, `:564-600`;
`local-1-arm-b/pipeline.json:466-735`; `test_window_record.py:1800-1859`.
Greps (the Grep tool; shapes noted): `review:` producers over scripts/*.py (positive: `acceptance.py:1157`); `word_let_go\(|word_kept\(`
(5 sites); `"match":` over fixtures/stories pipeline.json (all listed; `review:` only in local-1-arm-b); `not receipted` (positive
controls in tests); `split_overridden|_record_person_pass\(` in controller.py. Glob: no `read-main` worktree (memory pointer stale;
the root checkout matched the critic's origin/main lines, so it was used); `local-1-arm-b/**/*.json` (no manifest/windows,
positive control: the same Glob form lists `cart-1/work/windows/*`).
